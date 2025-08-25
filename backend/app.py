# backend/app.py

from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from rag_logic import process_document, get_response_from_query

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable Cross-Origin Resource Sharing

# Define the upload folder
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def home():
    """
    Root endpoint to test if the server is running.
    """
    return jsonify({
        "message": "RAG Chatbot Backend is running!",
        "status": "success",
        "available_endpoints": [
            "POST /api/upload - Upload PDF documents",
            "POST /api/chat - Chat with documents"
        ]
    })

@app.route('/api/upload', methods=['POST'])
def upload_file():
    """
    API endpoint to upload a document.
    """
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file and file.filename.endswith('.pdf'):
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)

        # Process the document to build the vector store
        success = process_document(file_path)
        if success:
            return jsonify({"message": f"File '{file.filename}' uploaded and processed successfully."}), 200
        else:
            return jsonify({"error": "Failed to process the document."}), 500
    else:
        return jsonify({"error": "Invalid file type. Only PDF is supported."}), 400


@app.route('/api/chat', methods=['POST'])
def chat():
    """
    API endpoint to handle chat queries.
    """
    data = request.get_json()
    user_query = data.get('message')

    if not user_query:
        return jsonify({"error": "No message provided"}), 400
        
    # Get the response from our RAG logic
    response = get_response_from_query(user_query)
    
    return jsonify(response)


if __name__ == '__main__':
    # Note: In a production environment, use a proper WSGI server like Gunicorn
    app.run(debug=True, port=5000, host='0.0.0.0')