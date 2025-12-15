---
sidebar_position: 2
---

# Setup & Configuration

Follow these steps to set up the RAG chatbot environment locally.

## Prerequisites

*   Python 3.10+
*   Node.js 18+
*   Qdrant (Cloud or Local Docker)
*   Neon Postgres (or any Postgres)
*   API Keys: OpenAI, Google Gemini

## Backend Setup

1.  Navigate to `backend/`:
    ```bash
    cd backend
    ```
2.  Create virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate  # Windows: venv\Scripts\activate
    ```
3.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
4.  Configure `.env`:
    ```bash
    cp .env.example .env
    # Edit .env with your API keys
    ```
5.  Run the server:
    ```bash
    uvicorn src.api.main:app --reload
    ```

## Frontend Setup

1.  Navigate to `website/`:
    ```bash
    cd website
    ```
2.  Install dependencies:
    ```bash
    npm install
    ```
3.  Start Docusaurus:
    ```bash
    npm start
    ```

## Ingestion

To index the book content, send a POST request to the ingest endpoint:

```bash
curl -X POST http://localhost:8000/api/v1/ingest \
  -H "X-API-Key: your_secret_key"
```

