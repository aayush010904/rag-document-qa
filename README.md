# HackRx Document QA System

An LLM-powered intelligent query-retrieval system that processes documents and provides contextual answers for insurance, legal, HR, and compliance domains.

## 🚀 Features

- **Multi-format Document Support**: PDF, DOCX, and email files
- **Semantic Search**: Uses Pinecone vector database for intelligent retrieval
- **Insurance Domain Optimized**: Specialized prompts for accurate policy information
- **Fast Response**: Async processing with Groq LLM integration
- **Token Efficient**: Optimized prompts with 35-word response limits
- **RESTful API**: FastAPI-based with proper authentication

## 📋 Requirements

- Python 3.10+
- Pinecone API Key
- Groq API Key

## 🛠️ Installation

1. **Clone/Download the project**

   ```bash
   cd document
   ```

2. **Set up Python environment**

   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   # source venv/bin/activate  # Linux/Mac
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Configuration**
   Create a `.env` file with:
   ```env
   GROQ_API_KEY=your_groq_api_key_here
   PINECONE_API_KEY=your_pinecone_api_key_here
   PINECONE_INDEX=your_pinecone_index_name
   ```

## 🏃‍♂️ Quick Start

1. **Start the API server**

   ```bash
   python app.py
   ```

   The server will start on `http://localhost:8000`

2. **Test with sample request**
   ```bash
   curl -X POST "http://localhost:8000/hackrx/run" \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer b689cc51239dbe57b19d7432235ab5fd0adc0ab7bd705f4cb51920ec4c53ce9e" \
     -d '{
       "documents": "https://example.com/policy.pdf",
       "questions": [
         "What is the grace period for premium payment?",
         "Does this policy cover maternity expenses?"
       ]
     }'
   ```

## 📁 Project Structure

```
document/
├── app.py                    # FastAPI application entry point
├── config.py                 # Environment configuration
├── document_processor.py     # Document text extraction (PDF/DOCX/Email)
├── vector_store.py          # Pinecone vector operations
├── llm_client.py            # Groq LLM integration
├── pipeline.py              # Main processing pipeline
├── requirements.txt         # Python dependencies
├── test_response_format.py  # Response format validation
└── README.md               # This file
```

## 🔧 Core Components

### **Document Processor** (`document_processor.py`)

- Extracts text from PDF, DOCX, and email files
- Handles multiple document formats intelligently
- Chunks text for optimal processing

### **Vector Store** (`vector_store.py`)

- Manages Pinecone vector database operations
- Converts text to embeddings using SentenceTransformer
- Performs semantic similarity search

### **LLM Client** (`llm_client.py`)

- Interfaces with Groq LLM API
- Optimized prompts for insurance domain
- Token-efficient response generation

### **Pipeline** (`pipeline.py`)

- Orchestrates the complete workflow
- Downloads documents from blob URLs
- Processes multiple questions asynchronously

## 🌐 API Endpoints

### `POST /hackrx/run`

Process documents and answer questions.

**Headers:**

```
Content-Type: application/json
Authorization: Bearer b689cc51239dbe57b19d7432235ab5fd0adc0ab7bd705f4cb51920ec4c53ce9e
```

**Request Body:**

```json
{
  "documents": "https://example.com/document.pdf",
  "questions": [
    "What is the waiting period for pre-existing diseases?",
    "Does this policy cover organ donor expenses?"
  ]
}
```

**Response:**

```json
{
  "answers": [
    "There is a waiting period of thirty-six (36) months for pre-existing diseases.",
    "Yes, medical expenses for organ donors are covered under specific conditions."
  ]
}
```

## 🎯 Supported Document Types

| Format | Extensions      | Description              |
| ------ | --------------- | ------------------------ |
| PDF    | `.pdf`          | Standard PDF documents   |
| Word   | `.docx`, `.doc` | Microsoft Word documents |
| Email  | `.eml`, `.msg`  | Email messages           |

## ⚡ Performance Features

- **Async Processing**: Handles multiple questions concurrently
- **Smart Chunking**: Optimized text segmentation for better retrieval
- **Vector Caching**: Efficient embedding storage and retrieval
- **Token Optimization**: Minimized LLM token usage

## 🔒 Security

- Bearer token authentication
- Input validation with Pydantic models
- Error handling with proper HTTP status codes
- Secure environment variable management

## 🧪 Testing

Run the response format test:

```bash
python test_response_format.py
```

This validates that the API returns responses in the correct JSON format.

## 📊 System Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Document      │    │   Text           │    │   Vector        │
│   Download      │───▶│   Extraction     │───▶│   Storage       │
│   (PDF/DOCX)    │    │   & Chunking     │    │   (Pinecone)    │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                                         │
┌─────────────────┐    ┌──────────────────┐             │
│   JSON          │    │   LLM            │             │
│   Response      │◀───│   Processing     │◀────────────┘
│   Generation    │    │   (Groq)         │
└─────────────────┘    └──────────────────┘
```

## 🎮 Usage Examples

### Insurance Policy Query

```json
{
  "documents": "https://example.com/health-policy.pdf",
  "questions": [
    "What is the maximum sum insured?",
    "Are dental treatments covered?",
    "What is the claim settlement ratio?"
  ]
}
```

### Legal Document Analysis

```json
{
  "documents": "https://example.com/contract.docx",
  "questions": [
    "What is the termination clause?",
    "Are there any penalty provisions?",
    "What is the governing law?"
  ]
}
```

## 🔧 Configuration

### Pinecone Setup

1. Create a Pinecone account
2. Create an index with dimension 384 (for SentenceTransformer model)
3. Add your API key and index name to `.env`

### Groq Setup

1. Get API key from Groq Console
2. Add to `.env` file

## 🚀 Deployment

For production deployment:

1. **Use a production ASGI server**

   ```bash
   pip install gunicorn
   gunicorn app:app -w 4 -k uvicorn.workers.UvicornWorker
   ```

2. **Environment Variables**
   Set all required environment variables in your deployment platform

3. **Health Check**
   The API includes built-in health monitoring through FastAPI's automatic docs

## 📝 License

This project is developed for HackRx competition.

## 🤝 Contributing

This is a competition submission. For questions or improvements, please refer to the development team.

---

**Built with ❤️ for HackRx Competition**
