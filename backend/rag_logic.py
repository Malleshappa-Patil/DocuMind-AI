# backend/rag_logic.py

import os
import sys
import shutil
from pypdf import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import GPT4AllEmbeddings
from gpt4all import GPT4All
import numpy as np
import warnings
warnings.filterwarnings("ignore")

# --- Global Variables ---
vector_store = None
embedding_model = None
llm = None
current_document = None  # Track current document
CHROMA_DB_DIR = "./chroma_db"

def initialize_models():
    """
    Initialize the embedding model and LLM. This is done separately to handle any download/loading issues.
    """
    global embedding_model, llm
    
    try:
        print("Initializing embedding model...")
        # Initialize embedding model
        embedding_model = GPT4AllEmbeddings(model_name="nomic-embed-text-v1.f16.gguf")
        print("Embedding model initialized successfully.")
        
        print("Initializing LLM...")
        # UPDATED: Switch to Mistral-7B-OpenOrca with larger context (8192 tokens native)
        # This model is stronger for summarization and RAG, auto-downloads if missing
        llm = GPT4All("mistral-7b-openorca.gguf2.Q4_0.gguf", n_ctx=4096, allow_download=True)
        print("LLM initialized successfully.")
        
        return True
    except Exception as e:
        print(f"Error initializing models: {e}")
        return False

def clear_vector_store():
    """
    Clear the existing vector store and database.
    """
    global vector_store
    vector_store = None
    
    # Remove the ChromaDB directory if it exists
    if os.path.exists(CHROMA_DB_DIR):
        try:
            shutil.rmtree(CHROMA_DB_DIR)
            print("Previous vector store cleared.")
        except Exception as e:
            print(f"Warning: Could not clear previous vector store: {e}")

def process_document(file_path):
    """
    Processes a PDF document, chunks the text, creates embeddings, and builds a vector store.
    """
    global vector_store, embedding_model, current_document
    
    # Initialize models if not already done
    if embedding_model is None:
        if not initialize_models():
            return False
    
    # Clear previous vector store for new document
    print("Clearing previous document data...")
    clear_vector_store()
    
    try:
        print(f"Processing new document: {file_path}")
        
        # Check if file exists
        if not os.path.exists(file_path):
            print(f"Error: File {file_path} does not exist.")
            return False
        
        # Store current document info
        current_document = os.path.basename(file_path)
        
        # Read PDF
        pdf_reader = PdfReader(file_path)
        text = ""
        
        print(f"Extracting text from {len(pdf_reader.pages)} pages...")
        for page_num, page in enumerate(pdf_reader.pages):
            try:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
                    print(f"Processed page {page_num + 1}")
            except Exception as e:
                print(f"Error processing page {page_num + 1}: {e}")
                continue

        if not text.strip():
            print("Error: Could not extract text from the PDF.")
            return False

        print(f"Extracted text length: {len(text)} characters")

        # Split text into chunks
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len
        )
        chunks = text_splitter.split_text(text=text)
        print(f"Created {len(chunks)} text chunks")

        if not chunks:
            print("Error: No text chunks were created.")
            return False

        # Create NEW vector store using ChromaDB
        print("Creating new vector store with ChromaDB...")
        vector_store = Chroma.from_texts(
            texts=chunks, 
            embedding=embedding_model,
            persist_directory=CHROMA_DB_DIR  # This will save the database locally
        )
        
        print(f"Document '{current_document}' processed and new vector store created successfully.")
        return True

    except Exception as e:
        print(f"An error occurred during document processing: {e}")
        import traceback
        traceback.print_exc()
        return False

def get_response_from_query(query):
    """
    Finds relevant document chunks and uses an LLM to generate a conversational response.
    """
    global vector_store, llm, current_document
    
    if vector_store is None:
        return {"reply": "Please upload a document first.", "citations": []}

    # Initialize models if not already done
    if llm is None:
        if not initialize_models():
            return {"reply": "Error: Could not initialize the language model.", "citations": []}

    try:
        print(f"Processing query for document '{current_document}': {query}")
        
        # Check for summarization keywords to adjust how much context we retrieve
        summarization_keywords = ['summarize', 'summary', 'overview', 'give me the gist']
        is_summarization_request = any(keyword in query.lower() for keyword in summarization_keywords)
        
        # UPDATED: Get more context for summaries (10 chunks) now that we have a larger context window; keep 3 for focused queries
        num_chunks_to_retrieve = 10 if is_summarization_request else 3
        
        # Search for relevant documents
        docs = vector_store.similarity_search(query=query, k=num_chunks_to_retrieve)

        if not docs:
            return {"reply": f"I couldn't find relevant information in the current document '{current_document}' to answer your question.", "citations": []}
        
        context = "\n\n".join([doc.page_content for doc in docs])
        print(f"Retrieved {len(docs)} relevant chunks from current document")

        # Create prompt with document context
        prompt_template = f"""Based on the following context from the document "{current_document}", please answer the question. Be concise and accurate.

Context:
{context}

Question: {query}

Answer:"""

        print("Generating response from LLM...")
        
        # Generate response
        response = llm.generate(
            prompt=prompt_template, 
            max_tokens=400,
            temp=0.7,
            top_p=0.9
        )
        
        print("Response generated successfully.")

        # Clean up the response
        response = response.strip()
        
        # Get citations
        citations = [doc.page_content for doc in docs]

        return {"reply": response, "citations": citations}

    except Exception as e:
        print(f"An error occurred during query processing: {e}")
        import traceback
        traceback.print_exc()
        return {"reply": "Sorry, an error occurred while processing your question. Please try again.", "citations": []}

# Initialize models when the module is imported
print("Initializing RAG system...")
initialize_models()