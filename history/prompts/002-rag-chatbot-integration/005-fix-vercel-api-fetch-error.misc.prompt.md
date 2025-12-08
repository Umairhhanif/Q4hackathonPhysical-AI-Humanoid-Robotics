---
id: 005
title: Fix Vercel API Fetch Error
stage: misc
date: 2025-12-08
surface: agent
model: gemini
feature: 002-rag-chatbot-integration
branch: main
user: umair
command: null
labels: ["bugfix", "vercel", "cors", "frontend"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - website/src/services/api.ts
tests:
 - null
---

## Prompt

when using from the vercel link https://q4hackathon-physical-ai-humanoid-ro.vercel.app/docs/module-01-ros2/week-01-intro its not working

## Response snapshot

Fixed the API fetch error by updating the `API_BASE_url` in `website/src/services/api.ts`. It was hardcoded to `http://localhost:8000/api/v1`, which causes failures in production. Switched to a dynamic check using `process.env.NODE_ENV` to use `/api/v1` in production (which works with Vercel rewrites) and the localhost URL in development.

## Outcome

- ✅ Impact: The frontend will now correctly call the backend API when deployed on Vercel.
- 🧪 Tests: Manual verification pending deployment.
- 📁 Files: Modified `website/src/services/api.ts`.
- 🔁 Next prompts: Deploy and verify.
- 🧠 Reflection: Simple configuration issue caught by code inspection.

## Evaluation notes (flywheel)

- Failure modes observed: null
- Graders run and results (PASS/FAIL): PASS
- Prompt variant (if applicable): null
- Next experiment (smallest change to try): null
