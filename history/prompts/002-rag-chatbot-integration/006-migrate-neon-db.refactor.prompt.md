---
ID: "006"
TITLE: "migrate-neon-db"
STAGE: "refactor"
DATE: "2025-12-08"
SURFACE: "agent"
MODEL: "active-model"
FEATURE: "rag-chatbot-integration"
BRANCH: "main"
USER: "umair"
COMMAND: "fix this please"
LABELS: ["database", "neon", "postgres", "migration", "asyncpg", "ssl"]
LINKS:
  SPEC: null
  TICKET: null
  ADR: null
  PR: null
FILES_YAML:
  - "backend/src/core/database.py"
  - "backend/.env"
TESTS_YAML:
  - "verify_db_fix.py"
---

# PROMPT_TEXT
my server should be on Neon Serverless Postgres database not on local

# RESPONSE_TEXT
Migrated database connection to Neon Serverless Postgres.
- Updated `backend/src/core/database.py` to handle `sslmode=require` compatibility with `asyncpg`.
- Verified connection using `verify_db_fix.py`.
- Restarted backend server to apply changes.
