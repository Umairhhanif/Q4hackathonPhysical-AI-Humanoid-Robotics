# Quickstart: RAG Chatbot Integration

## Prerequisites

- Python 3.10+
- Node.js 18+
- Docker (optional, for local Postgres/Qdrant if not using cloud)

## Environment Variables

Create a `.env` file in the `backend/` directory:

```bash
# OpenAI (for Embeddings)
OPENAI_API_KEY=sk-...

# Google Gemini (for Chat)
GOOGLE_API_KEY=AIza...

# Qdrant (Vector DB)
QDRANT_URL=https://...
QDRANT_API_KEY=...

# Neon (Postgres)
DATABASE_URL=postgresql://...

# Security
API_SECRET=your_secret_key_for_ingest
```

## Setup Backend

1. Navigate to `backend/`:
   ```bash
   cd backend
   ```
2. Create and activate venv:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the server:
   ```bash
   uvicorn src.api.main:app --reload
   ```

## Setup Frontend (Docusaurus)

1. Navigate to `website/`:
   ```bash
   cd website
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Start the dev server:
   ```bash
   npm start
   ```

## Ingestion

To index the book content:

```bash
curl -X POST http://localhost:8000/ingest \
  -H "X-API-Key: your_secret_key_for_ingest"
```

