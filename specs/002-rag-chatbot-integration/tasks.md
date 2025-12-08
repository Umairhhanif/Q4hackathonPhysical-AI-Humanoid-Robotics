# Tasks: RAG Chatbot Integration

**Feature**: RAG Chatbot Integration
**Status**: Planned
**Spec**: [spec.md](spec.md)
**Plan**: [plan.md](plan.md)

## Implementation Strategy

We will implement the RAG chatbot in a layered approach, starting with the backend infrastructure (ingestion, vector store, DB), followed by the core retrieval/chat API logic, and finally the Docusaurus frontend integration.

- **MVP Scope**: User Story 1 (Global QA) - Ingestion, Basic Chat, Global Widget.
- **Incremental**: User Story 2 (Context QA) adds the selection logic on top of the working chat.
- **Docs**: User Story 3 is documentation, which we will write as we build or immediately after.

## Phase 1: Setup

**Goal**: Initialize the project environment and dependencies for both backend (FastAPI) and frontend (Docusaurus).

- [x] T001 [P] Create backend directory structure and virtual environment in `backend/`
- [x] T002 [P] Create `backend/requirements.txt` with FastAPI, QdrantClient, OpenAI, Google-GenAI, SQLAlchemy/AsyncPG
- [x] T003 Create `backend/.env` template (and local `.env`) with placeholders for API keys
- [x] T004 Initialize FastAPI application skeleton in `backend/src/api/main.py`
- [x] T005 Configure CORS and basic middleware in `backend/src/api/main.py`

## Phase 2: Foundational (Entities & DB)

**Goal**: Establish data models and database connections (Neon Postgres & Qdrant) required for all user stories.

- [x] T006 [P] Implement Database config and session factory in `backend/src/core/database.py` (Neon Postgres)
- [x] T007 [P] Implement Qdrant client singleton in `backend/src/services/vector_store.py`
- [x] T008 [P] Define SQLAlchemy models for Interaction Log in `backend/src/models/chat.py`
- [x] T009 [P] Define Pydantic models for API request/response in `backend/src/models/api.py` (ChatRequest, ChatResponse)
- [x] T010 [P] Create Qdrant collection initialization script/function in `backend/src/services/vector_store.py`

## Phase 3: User Story 1 (Global Book QA)

**Goal**: Enable users to ask questions about the entire book content. Includes ingestion pipeline and core RAG flow.

### Setup & Ingestion
- [x] T011 [US1] Implement Markdown chunking logic (recursive character splitter) in `backend/src/services/ingest.py`
- [x] T012 [US1] Implement Embedding generation service (OpenAI) in `backend/src/services/llm.py`
- [x] T013 [US1] Implement `ingest_documents` function to process `docs/` folder and upload to Qdrant in `backend/src/services/ingest.py`
- [x] T014 [US1] Create API endpoint `POST /ingest` in `backend/src/api/routes/ingest.py` to trigger indexing

### Retrieval & Generation
- [x] T015 [US1] Implement Hybrid/Dense retrieval logic in `backend/src/services/retrieval.py`
- [x] T016 [US1] Implement Google Gemini generation service in `backend/src/services/llm.py`
- [x] T017 [US1] Implement RAG orchestration (Retrieve -> Prompt -> Generate) in `backend/src/services/chat.py`
- [x] T018 [US1] Create API endpoint `POST /chat` in `backend/src/api/routes/chat.py` (Global QA mode)

### Frontend Integration
- [x] T019 [US1] Install frontend dependencies (if any needed for UI components) in `website/package.json`
- [x] T020 [US1] Create `ChatWidget` component in `website/src/components/ChatWidget.tsx`
- [x] T021 [US1] Implement API client for chat endpoint in `website/src/services/api.ts`
- [x] T022 [US1] Add `ChatWidget` to `website/src/theme/Root.tsx` (or Layout) to make it global

### Validation
- [ ] T023 [US1] Verify ingestion populates Qdrant collection correctly
- [ ] T024 [US1] Functional test: Ask general question about the book via API and verify citation

## Phase 4: User Story 2 (Context-Specific QA)

**Goal**: Enable "Select text -> Ask AI" workflow.

- [x] T025 [P] [US2] Update `ChatRequest` model to include optional `selected_text` in `backend/src/models/api.py`
- [x] T026 [US2] Update RAG orchestration in `backend/src/services/chat.py` to prioritize `selected_text` in context
- [x] T027 [US2] Implement frontend text selection listener in `website/src/theme/Root.tsx` (or dedicated hook)
- [x] T028 [US2] Create "Ask AI" tooltip/button component in `website/src/components/SelectionTooltip.tsx`
- [x] T029 [US2] Connect selection action to open ChatWidget with context in `website/src/components/ChatWidget.tsx`

## Phase 5: User Story 3 (Documentation)

**Goal**: Document the architecture for readers (Developers).

- [x] T030 [US3] Create `website/docs/module-05-rag/01-architecture.md` with system diagrams
- [x] T031 [US3] Create `website/docs/module-05-rag/02-setup.md` with environment setup instructions
- [x] T032 [US3] Create `website/docs/module-05-rag/03-code-walkthrough.md` explaining key snippets

## Phase 6: Polish & Deployment

**Goal**: Production readiness.

- [x] T033 [P] Implement async interaction logging to Neon Postgres in `backend/src/services/logging.py`
- [x] T034 [P] Add error handling and user-friendly messages in `backend/src/api/routes/chat.py`
- [x] T035 Configure Vercel deployment settings (e.g., `vercel.json` for backend if deploying there)
- [x] T036 Final manual acceptance test of full flow on local build

## Dependencies

- **US1** requires Phase 1 & 2 complete.
- **US2** requires US1's Chat Endpoint and Widget to be functional.
- **US3** is independent but best done after US1 implementation details are stable.

## Parallel Execution Examples

- **Backend vs Frontend**: T020 (Frontend Widget) can be built in parallel with T015 (Backend Retrieval) using mocked API responses.
- **Ingestion vs Chat**: T011 (Ingestion logic) and T016 (Gemini integration) are largely independent until the orchestration step (T017).
