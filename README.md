# 📚 Semantic Book Recommender using LLMs

This is my personal implementation of a **Semantic Book Recommender System** powered by **Large Language Models (LLMs)**, **vector databases**, and an interactive **Gradio web app**.

The project is based on the freeCodeCamp course:  
➡️ [Build a Semantic Book Recommender with LLMs – Full Course]([https://www.youtube.com/watch?v=8bbMHRn3Hjo](https://www.youtube.com/watch?v=Q7mS1VHm3Yw&list=WL&index=3))

I’m rebuilding it from scratch to improve my understanding of LLMs, embeddings, zero-shot classification, and real-world NLP systems.

---

## 🧠 Features

- ✅ Clean and explore book metadata and descriptions
- 🧠 Use OpenAI embeddings for semantic search
- 🔎 Build a vector database using **Chroma**
- 🧾 Classify books using **zero-shot** techniques (Fiction / Non-fiction)
- 🎭 Perform sentiment and emotion analysis on summaries
- 🖥️ Deploy a full interactive recommendation UI with **Gradio**

---

## 📁 Project Structure

| File/Folder              | Description |
|--------------------------|-------------|
| `data-exploration.ipynb` | Clean and analyze the book dataset |
| `vector-search.ipynb`    | Create semantic vectors and search similar books |
| `text-classification.ipynb` | Classify books as Fiction or Non-fiction using LLMs |
| `sentiment-analysis.ipynb` | Extract tone and emotions from book summaries |
| `gradio-dashboard.py`    | Gradio-based web app for user interaction |
| `.env`                   | Environment file with API keys (you must create it) |
| `requirements.txt`       | List of all required Python packages |

---
## 📥 Dataset

This project uses a dataset available on [Kaggle](https://www.kaggle.com/).  
The notebook includes instructions for downloading it using the `kagglehub` package.

To use the Kaggle API:

1. 🔐 Create an API token from your Kaggle account  
   (Go to https://www.kaggle.com/account → "Create New API Token")

2. 🧰 Install the required package:

```bash
pip install kagglehub 




