# 📚 AI Book Recommender

An intelligent book recommender system that uses **Hugging Face embeddings**, **LangChain**, **ChromaDB**, and **Gradio** to provide genre prediction, sentiment analysis, and smart recommendations — all in an interactive UI.

---

## 🚀 Features

- 📖 Upload a CSV of books (title, author, description)
- 📚 Generate embeddings using **HuggingFace (MiniLM-L6-v2)**
- 🔍 Semantic search for similar books
- 🎭 Sentiment and emotion analysis
- 🧠 Zero-shot genre classification
- 🌐 Intuitive **Gradio** web interface

---

## 🌐 Technologies Used

| Technology                   | Description                                                          |
|------------------------------|----------------------------------------------------------------------|
| 🐍 Python 3.11               | Core programming language                                            |
| 🤗 HuggingFace Transformers  | For pretrained embeddings & classification models                   |
| 🧠 LangChain                 | Orchestrates LLMs and embeddings using `HuggingFaceEmbeddings`       |
| 📦 ChromaDB                 | Vector database for similarity search                                |
| 🖼️ Gradio                   | Web UI for input/output and interaction                             |
| 📊 Pandas                   | Dataset loading and manipulation                                     |
| 📈 Seaborn, Matplotlib       | Data visualization tools                                             |
| 🧾 Zero-shot Classification | Genre tagging without training                                       |
| 🎭 Sentiment Analysis        | Detects tone and emotional context of books                         |

---

## 📁 Project Structure

| File/Folder                | Description                                             |
|----------------------------|---------------------------------------------------------|
| `data-exploration.ipynb`   | Clean and analyze the book dataset                      |
| `vector-search.ipynb`      | Create semantic vectors and search similar books        |
| `text-classification.ipynb`| Classify books as Fiction or Non-fiction using LLMs     |
| `sentiment-analysis.ipynb` | Extract tone and emotions from book summaries           |
| `gradio-dashboard.py`      | Gradio-based web app for user interaction               |
| `.env`                     | Environment file with API keys (you must create it)     |
| `requirements.txt`         | List of all required Python packages                    |

---

## 📥 Dataset

This project uses a dataset available on [Kaggle](https://www.kaggle.com/).  
The notebook includes instructions for downloading it using the `kagglehub` package.

To use the Kaggle API:

1. 🔐 Create an API token from your Kaggle account  
   (Go to [kaggle.com/account](https://www.kaggle.com/account) → "Create New API Token")

2. 🧰 Install the required package:

```bash
pip install kagglehub
