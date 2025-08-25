# DocuMind-AI

A Retrieval-Augmented Generation (RAG) Chatbot that allows users to upload PDF documents, process their content, and query the document via natural language questions. The chatbot leverages local AI models (GPT4All) and a vector store (ChromaDB) to provide accurate responses with citations.

## Features
- Upload and process PDF files.
- Extract text, chunk it, and create embeddings for a vector database.
- Retrieve relevant text chunks based on user queries.
- Generate concise responses using a local LLM (Mistral-7B-OpenOrca).
- Support for summarization requests (e.g., "summarise the pdf").
- Local execution with no cloud dependencies.

## Prerequisites
- Python 3.8 or higher.
- Git (for cloning the repository).
- Approximately 5-6 GB of free disk space (for model downloads).

## Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/your-username/rag-chatbot.git
   cd rag-chatbot

2. **Set Up a Virtual Environment
    ```bash
    python -m venv venv
    venv/bin/activate  # On Windows venv\Scripts\activate

3. **Install Dependencies
    Install the required Python packages from the requirements.txt file:
    ```bash
    pip install -r backend/requirements.txt
    ```
    Note: The first run will download the Mistral-7B-OpenOrca model (~4GB), which may take time depending on your internet speed.

4. **Run the Application
    Navigate to the backend directory and start the Flask server:
    ```bash