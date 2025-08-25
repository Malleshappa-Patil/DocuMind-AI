# DocuMind-AI

---

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

---

## Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/your-username/rag-chatbot.git
   cd rag-chatbot

2. **Set Up a Virtual Environment**
    ```bash
    python -m venv venv
    venv/bin/activate  # On Windows venv\Scripts\activate

3. **Install Dependencies**
    Install the required Python packages from the requirements.txt file:
    ```bash
    pip install -r backend/requirements.txt
    ```
    Note: The first run will download the Mistral-7B-OpenOrca model (~4GB), which may take time depending on your internet speed.

4. **Run the Application**
    Navigate to the backend directory and start the Flask server:
    ```bash
    cd backend
    python app.py
    ```
    The server will run on http://0.0.0.0:5000 in debug mode.

5. Access the Frontend Open frontend/index.html in a web browser. Alternatively, serve it with a local server (e.g., python -m http.server in the frontend directory) to handle file uploads correctly.

---

## Usage

1. **Upload a PDF:** Use the "Upload Your PDF Document" section on the webpage to select and upload a PDF

2. **Process the Document:** The backend will extract text, chunk it, and build a vector store.

3. **Chat:** Enter a query (e.g., "summarise the pdf" or "what is covered?") in the chat input and press Enter or click "Send".

4. **View Responses:** Receive a response with relevant citations from the document.


## Folder Structure

```plantext
DocuMind-AI/
├── backend/
│   ├── __pycache__/
│   ├── chroma_db/
│   ├── uploads/
│   │   ├── Insurance.pdf
│   ├── git_cheat_sheet.pdf
│   ├── venv/
│   │   ├── bin/
│   │   ├── include/
│   │   ├── lib/
│   │   └── share/
│   ├── .gitignore
│   ├── pyvenv.cfg
│   ├── app.py
│   ├── rag_logic.py
│   └── requirements.txt
├── frontend/
│   ├── index.html
├── README.md
```

## Directory Details

1. **backend/:** Contains the server-side code and data.
    1. **__pycache__:** Python bytecode cache.
    2. **chroma_db/:** Directory for the Chroma vector store (persists document embeddings).
    3. **uploads/:** Stores uploaded PDF files (e.g., Insurance.pdf).
    4. **venv/:** Virtual environment for Python dependencies.
    5. **app.py:** Flask API for handling uploads and chat queries.
    6. **rag_logic.py:** Core RAG logic (text extraction, chunking, embedding, LLM response generation).
    7. **requirements.txt:** List of Python dependencies.


2. **frontend/:** Contains the client-side HTML interface.
    1. **index.html:** The web UI for uploading PDFs and chatting.

3. **README.md:** This file, providing project documentation.

---

## Project Files

1. **app.py**
-    The Flask backend server with endpoints:
    - /: Health check.
    - /api/upload: Handles PDF uploads and processing.
    - /api/chat: Processes user queries and returns responses.

2. **rag_logic.py**
-    Implements the RAG pipeline:
    - Initializes GPT4All models (Mistral-7B-OpenOrca for LLM, nomic-embed-text-v1 for embeddings).
    - Processes PDFs into chunks and builds a Chroma vector store.
    - Retrieves relevant chunks and generates responses with citations.

3. **index.html**
- A simple HTML interface with:
    - A section to upload PDFs.
    - A chat window to input queries and display responses.
    - Basic CSS for styling.

4. **requirements.txt**
- Lists dependencies including Flask, LangChain, GPT4All, and ChromaDB.

---

## Contributing
- Feel free to fork this repository, submit issues, or create pull requests to enhance the project. Suggestions for improvements include:
    - Support for multiple documents.
    - Better error handling for large PDFs.
    - Integration with larger AI models.

---

## Acknowledgements
- Built with inspiration from LangChain and GPT4All communities.
- Uses ChromaDB for efficient vector storage.

---

## 📧 Contact

For any questions or feedback regarding this project, feel free to reach out.

-   **Email:** `mdpatil2004@gmail.com`

Thank you for checking out the project!
