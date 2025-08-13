"""
Book Recommendation System with Semantic Search
Powered by LangChain, HuggingFace Embeddings, and ChromaDB
"""

# Core libraries
import pandas as pd
import numpy as np
from typing import List, Tuple
import gradio as gr

# LangChain components (updated to use community packages)
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

# Environment variables
from dotenv import load_dotenv
load_dotenv()

# ======================
# DATA PREPARATION
# ======================

def load_and_prepare_book_data(filepath: str) -> pd.DataFrame:
    """
    Load book data from CSV and prepare it for recommendation system
    Args:
        filepath: Path to the CSV file containing book data
    Returns:
        Prepared pandas DataFrame
    """
    # Load book data with emotions
    books = pd.read_csv(filepath)
    
    # Enhance thumbnail URLs with higher resolution
    books["large_thumbnail"] = (
        books["thumbnail"] + "&fife=w800"  # Higher resolution parameter
    )
    
    # Handle missing thumbnails with default image
    books["large_thumbnail"] = np.where(
        books["large_thumbnail"].isna(),
        "cover-not-found.jpg",  # Default image path
        books["large_thumbnail"],
    )
    
    return books

# Load and prepare book data
books = load_and_prepare_book_data("books_with_emotions.csv")

# ======================
# VECTOR DATABASE SETUP
# ======================

def initialize_vector_db(text_file: str = "tagged_description.txt") -> Chroma:
    """
    Initialize and return the vector database with local embeddings
    Args:
        text_file: Path to the text file containing book descriptions
    Returns:
        Chroma vector database instance
    """
    try:
        # 1. Load documents with UTF-8 encoding handling
        print("Loading documents...")
        raw_documents = TextLoader(text_file, encoding="utf-8").load()
        
        # 2. Configure text splitting with overlap for context preservation
        text_splitter = CharacterTextSplitter(
            chunk_size=800,       # Optimal size for book descriptions
            chunk_overlap=200,     # Preserves context between chunks
            separator="\n\n",      # Split by paragraphs first
            length_function=len,   # Count characters for chunk size
        )
        
        # Split documents into chunks
        print("Splitting documents into chunks...")
        documents = text_splitter.split_documents(raw_documents)
        
        # 3. Initialize local embeddings model (no API calls needed)
        print("Initializing embeddings model...")
        embeddings = HuggingFaceEmbeddings(
            model_name="all-MiniLM-L6-v2",  # Efficient local model
            model_kwargs={"device": "cpu"}, # Change to "cuda" if GPU available
            encode_kwargs={"normalize_embeddings": True}  # Better for similarity
        )
        
        # 4. Create persistent vector store
        print("Creating vector database...")
        db = Chroma.from_documents(
            documents,
            embedding=embeddings,
            persist_directory="./chroma_db"  # Saves to disk for reuse
        )
        
        print("Vector database initialized successfully!")
        return db
        
    except Exception as e:
        print(f"Error initializing vector database: {str(e)}")
        raise

# Initialize the vector database
db_books = initialize_vector_db()

# ======================
# RECOMMENDATION LOGIC
# ======================

def retrieve_semantic_recommendations(
        query: str,
        category: str = None,
        tone: str = None,
        initial_top_k: int = 50,
        final_top_k: int = 16,
) -> pd.DataFrame:
    """
    Retrieve books based on semantic similarity and filters
    Args:
        query: Text description to match against
        category: Filter by genre/category
        tone: Filter by emotional tone
        initial_top_k: First-stage results (broader search)
        final_top_k: Final returned results (after filtering)
    Returns:
        DataFrame of recommended books
    """
    try:
        # 1. Semantic search in vector database
        recs = db_books.similarity_search(query, k=initial_top_k)
        
        # 2. Convert to ISBN list (assuming first token in each chunk is ISBN)
        books_list = [int(rec.page_content.strip('"').split()[0]) for rec in recs]
        
        # 3. Get full book data from our DataFrame
        book_recs = books[books["isbn13"].isin(books_list)].head(initial_top_k)
        
        # 4. Apply category filter if specified
        if category and category != "All":
            book_recs = book_recs[book_recs["simple_categories"] == category]
        
        # 5. Apply emotion-based sorting if tone specified
        if tone and tone != "All":
            tone_mapping = {
                "Happy": "joy",
                "Surprising": "surprise",
                "Angry": "anger",
                "Suspenseful": "fear",
                "Sad": "sadness"
            }
            if tone in tone_mapping:
                book_recs = book_recs.sort_values(by=tone_mapping[tone], ascending=False)
        
        return book_recs.head(final_top_k)
    
    except Exception as e:
        print(f"Error in recommendation retrieval: {str(e)}")
        return pd.DataFrame()  # Return empty DataFrame on error

# ======================
# PRESENTATION LAYER
# ======================

def create_book_card(row: pd.Series) -> str:
    """
    Generate HTML card for a book recommendation
    Args:
        row: Pandas Series containing book data
    Returns:
        HTML string for the book card
    """
    # Format authors list naturally
    authors_split = row["authors"].split(";")
    if len(authors_split) == 2:
        authors_str = f"{authors_split[0]} and {authors_split[1]}"
    elif len(authors_split) > 2:
        authors_str = f"{', '.join(authors_split[:-1])}, and {authors_split[-1]}"
    else:
        authors_str = row["authors"]
    
    # Create star rating display
    stars = "★" * int(round(row["average_rating"])) + "☆" * (5 - int(round(row["average_rating"])))
    
    # Truncate description for card display
    short_desc = " ".join(row["description"].split()[:20]) + "..." if pd.notna(row["description"]) else "No description available"
    
    # Return HTML card with all book information
    return f"""
    <div class='book-card'>
        <img class='thumbnail' src='{row['large_thumbnail']}' alt='{row['title']}'>
        <div class='book-title'>{row['title']}</div>
        <div class='book-author'>By {authors_str}</div>
        <div class='book-desc'>{short_desc}</div>
        <div class='rating'>
            {stars} ({row['average_rating']:.1f}/5)
        </div>
    </div>
    """

def recommend_books(query: str, category: str, tone: str) -> List[Tuple[str, str]]:
    """
    Main recommendation function for Gradio interface
    Args:
        query: User's search query
        category: Selected category filter
        tone: Selected emotional tone filter
    Returns:
        List of tuples (image_path, html_card) for display
    """
    try:
        # Get recommendations from our semantic search
        recommendations = retrieve_semantic_recommendations(query, category, tone)
        
        # Return empty list if no recommendations found
        if recommendations.empty:
            return []
        
        # Format results for Gradio Gallery
        return [
            (row["large_thumbnail"], create_book_card(row))
            for _, row in recommendations.iterrows()
        ]
    
    except Exception as e:
        print(f"Error in recommendation pipeline: {str(e)}")
        return []

# ======================
# GRADIO INTERFACE
# ======================

# Custom CSS for professional styling
custom_css = """
:root {
    --primary: #4f46e5;
    --secondary: #f9fafb;
    --accent: #10b981;
    --text: #111827;
    --border: #e5e7eb;
}

.gradio-container {
    font-family: 'Inter', sans-serif;
    max-width: 1200px !important;
    margin: 0 auto !important;
}

/* Dark mode support */
.dark .gradio-container {
    --text: #f3f4f6;
    --secondary: #1f2937;
}

/* Header styling */
h1 {
    font-size: 2.5rem !important;
    background: linear-gradient(90deg, var(--primary), var(--accent));
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent;
    margin-bottom: 1rem !important;
    text-align: center;
}

/* Book card styling */
.book-card {
    padding: 1rem;
    background: var(--secondary);
    border-radius: 8px;
    height: 100%;
    display: flex;
    flex-direction: column;
    transition: transform 0.2s ease;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.book-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 4px 8px rgba(0,0,0,0.15);
}

.thumbnail {
    border-radius: 8px;
    height: 200px;
    width: 100%;
    object-fit: cover;
    margin-bottom: 0.5rem;
}

.book-title {
    font-weight: 600;
    margin: 0.5rem 0;
    color: var(--text);
    font-size: 1rem;
    line-height: 1.3;
}

.book-author {
    color: var(--text);
    opacity: 0.8;
    font-size: 0.9rem;
    margin-bottom: 0.5rem;
    font-style: italic;
}

.book-desc {
    color: var(--text);
    opacity: 0.9;
    font-size: 0.9rem;
    flex-grow: 1;
    margin-bottom: 0.5rem;
    line-height: 1.4;
}

.rating {
    display: flex;
    align-items: center;
    color: #f59e0b;
    font-size: 0.9rem;
    margin-top: auto;
}

/* Search input styling */
textarea {
    min-height: 80px !important;
}
"""

# Create dropdown options from book data
categories = ["All"] + sorted(books["simple_categories"].dropna().unique().tolist())
tones = ["All", "Happy", "Surprising", "Angry", "Suspenseful", "Sad"]

# Build the Gradio interface
with gr.Blocks(theme=gr.themes.Soft(), css=custom_css) as app:
    # Header section
    gr.Markdown("""
    <div style='text-align: center; margin-bottom: 2rem;'>
        <h1>📚 BookMatch AI</h1>
        <p style='font-size: 1.1rem; color: #6b7280;'>
            Discover your next favorite book with semantic search and emotional matching
        </p>
    </div>
    """)
    
    # Search controls
    with gr.Row():
        search_input = gr.Textbox(
            label="Describe your ideal book:",
            placeholder="e.g., 'A sci-fi adventure about time travel with complex characters'",
            lines=3,
            container=False
        )
        
    with gr.Row():
        category_filter = gr.Dropdown(
            choices=categories,
            label="Filter by Category",
            value="All",
            interactive=True
        )
        tone_filter = gr.Dropdown(
            choices=tones,
            label="Filter by Mood",
            value="All",
            interactive=True
        )
        search_btn = gr.Button(
            "Find Books",
            variant="primary",
            size="lg"
        )
    
    # Results display
    gr.Markdown("## Recommended Books")
    results_gallery = gr.Gallery(
        label="",
        columns=4,
        rows=4,
        height="auto",
        object_fit="cover"
    )
    
    # Footer
    gr.Markdown("""
    <div style='text-align: center; margin-top: 2rem; color: #6b7280; font-size: 0.9rem;'>
        Powered by HuggingFace embeddings • ChromaDB • LangChain
    </div>
    """)
    
    # Event handling - connect button click to recommendation function
    search_btn.click(
        fn=recommend_books,
        inputs=[search_input, category_filter, tone_filter],
        outputs=results_gallery
    )

# Launch the app
if __name__ == "__main__":
    app.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False  
    )
