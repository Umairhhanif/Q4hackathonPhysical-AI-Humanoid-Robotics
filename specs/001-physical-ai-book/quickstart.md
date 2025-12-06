# Quickstart: Physical AI Book

## Prerequisites
- Node.js 18+
- Python 3.10+
- Docker (optional, for Qdrant/Postgres local)

## 1. Setup Project
```bash
git clone <repo-url>
cd <repo-name>
```

## 2. Frontend (Website)
```bash
cd website
npm install
npm start
# Opens at http://localhost:3000
```

## 3. Backend (RAG API)
```bash
cd backend
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
uvicorn src.api.main:app --reload
# Runs at http://localhost:8000
```

## 4. Validation
- **Build**: `npm run build` (in website/)
- **Lint**: `npm run lint`
- **Test**: `npm test`
