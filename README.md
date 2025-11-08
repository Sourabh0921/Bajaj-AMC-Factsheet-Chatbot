# Bajaj AMC Factsheet Chatbot

A Streamlit-based chatbot application that processes Bajaj AMC fund factsheets and answers questions using RAG (Retrieval-Augmented Generation) technology.

## Features

- **Document Processing**: Upload and process PDF documents (fund factsheets)
- **OCR Support**: Extract text from image-based PDFs using Tesseract OCR
- **Vector Search**: FAISS-based vector similarity search for document retrieval
- **AI-Powered Responses**: ChatGroq LLM integration for intelligent Q&A
- **Clean UI**: Streamlit interface with custom styling
- **Real-time Processing**: Instant document embedding and query responses

## Project Structure

```
├── main.py                     # Main Streamlit application
├── requirements.txt            # Python dependencies
├── Dockerfile                 # Docker configuration
├── .env                       # Environment variables (API keys)
├── README.md                  # Project documentation
├── src/                       # Source code modules
│   ├── __init__.py
│   ├── chat_chain.py          # LLM chain and query handling
│   ├── file_processing.py     # PDF text extraction with OCR
│   ├── utils.py               # Utility functions
│   ├── vector_store.py        # Vector embedding and FAISS storage
│   └── src/
│       └── vector_store.py    # Alternative vector store implementation
├── static/
│   └── custom_styles.css      # Custom CSS styling
└── .vscode/
    └── settings.json          # VS Code configuration
```

## Technology Stack

- **Frontend**: Streamlit
- **LLM**: ChatGroq (openai/gpt-oss-120b model)
- **Embeddings**: Google Generative AI Embeddings
- **Vector Database**: FAISS
- **Document Processing**: PyPDF2, pdf2image, pytesseract
- **OCR**: Tesseract OCR
- **Deployment**: Docker, Render

## Setup Instructions

### Prerequisites

- Python 3.9+
- Tesseract OCR
- Docker (optional)

### Local Development

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Bajaj_Chat_with_Doc
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Install system dependencies (Ubuntu/Debian)**
   ```bash
   sudo apt-get update
   sudo apt-get install tesseract-ocr tesseract-ocr-eng libtesseract-dev poppler-utils
   ```

5. **Configure environment variables**
   Create a `.env` file with your API keys:
   ```env
   GOOGLE_API_KEY=your_google_api_key
   GROQ_API_KEY=your_groq_api_key
   HUGGINGFACEHUB_API_TOKEN=your_huggingface_token
   ```

6. **Run the application**
   ```bash
   streamlit run main.py
   ```

### Docker Deployment

1. **Build Docker image**
   ```bash
   docker build -t bajaj-chat-app .
   ```

2. **Run container**
   ```bash
   docker run -p 8501:10000 bajaj-chat-app
   ```


### Data Flow:
```
[User] → [Streamlit UI] → [handle_query()] → [ChatGroq LLM]
                                         ↓
[Cleaned Response] ← [clean_response()] ← [Raw Response]
                                         ↓
[Vector Store] → [Document Retrieval] → [Context Docs]
```

