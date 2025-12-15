ID: "002"
TITLE: "Debug Ask the Book AI Connection Error"
STAGE: "misc"
DATE_ISO: "2025-12-15"
SURFACE: "agent"
MODEL: "gemini-2.0-flash-exp"
FEATURE: "general"
BRANCH: "main"
USER: "Umairhhanif"
COMMAND: "npm run start"
LABELS: ["debug", "frontend", "backend", "connection-error", "fastapi"]
LINKS:
  SPEC: null
  TICKET: null
  ADR: null
  PR: null
FILES_YAML: 
  - E:\Speckithackhaton\website\src\components\ChatWidget.tsx
  - E:\Speckithackhaton\backend\src\api\main.py
TESTS_YAML: 
PROMPT_TEXT: |
  facing this error [Image showing 'Ask the Book' modal with 'Error connecting to AI.']
RESPONSE_TEXT: |
  Diagnosed that the backend server was not running.
  "Ask the Book" component tries to reach `http://localhost:8000/api/v1/chat`.
  Started the backend server using `uvicorn src.api.main:app` in the background.
  Identified potential missing configuration: `backend/.env` file is missing, which might cause downstream errors with OpenAI/Qdrant connection.
  Advised user to create `.env` if they encounter further errors.
