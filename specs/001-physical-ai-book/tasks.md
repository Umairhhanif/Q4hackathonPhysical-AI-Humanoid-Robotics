---

description: "Task list for Physical AI Book implementation"
---

# Tasks: Physical AI & Humanoid Robotics Book

**Input**: Design documents from `/specs/001-physical-ai-book/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/
**Tests**: Integrated into tasks where critical.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [x] T001 Create project directory structure (website/, backend/) per plan in `specs/001-physical-ai-book/plan.md`
- [x] T002 Initialize Docusaurus v3 project in `website/`
- [x] T003 Initialize FastAPI backend with venv and requirements in `backend/`
- [x] T004 [P] Create `website/src/css/custom.css` with basic Neon variables (colors, fonts)
- [x] T005 [P] Configure Prettier and ESLint for `website/`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T006 Install and configure `rehype-citation` in `website/docusaurus.config.ts`
- [x] T007 Create empty `website/references.bib` for citation management
- [x] T008 Setup Backend Core Config in `backend/src/core/config.py` (Env vars for OpenAI, Qdrant)
- [x] T009 Create Qdrant connection utility in `backend/src/services/vector_store.py`
- [x] T010 Create OpenAI client utility in `backend/src/services/llm.py`
- [x] T011 Setup basic FastAPI app structure in `backend/src/api/main.py` with CORS enabled

**Checkpoint**: Foundation ready - Docusaurus builds, Backend starts, DB connections configured.

---

## Phase 3: User Story 1 - Reader Accesses Technical Content (Priority: P1) 🎯 MVP

**Goal**: A deployable Docusaurus site with the first chapters of content and the custom Neon theme applied.

**Independent Test**: Run `npm start` in `website/`, verify Theme colors/buttons, navigate to "Physical AI Foundations".

### Implementation for User Story 1

- [x] T012 [US1] Update `website/src/css/custom.css` to implement full Neon Theme (Glow buttons, Dark bg)
- [x] T013 [US1] Update `website/docusaurus.config.ts` sidebar and navbar configuration
- [x] T014 [P] [US1] Create "Physical AI Foundations" chapter in `website/docs/01-foundations.md`
- [x] T015 [P] [US1] Create "Humanoid Robotics Fundamentals" chapter in `website/docs/02-humanoids.md`
- [x] T016 [US1] Create Landing Page with Neon Hero section in `website/src/pages/index.tsx`
- [x] T017 [US1] Create GitHub Actions workflow for Pages deployment in `.github/workflows/deploy.yml`

**Checkpoint**: Site is visually complete and has initial content.

---

## Phase 4: User Story 2 - User Queries RAG Chatbot (Priority: P1)

**Goal**: A functional Chat Widget embedded in the site that answers questions using the backend RAG API.

**Independent Test**: Send curl request to `/api/v1/chat` -> receive answer. Use Chat Widget on site -> receive answer.

### Backend Implementation
- [x] T018 [P] [US2] Define Pydantic models for Chat/Feedback in `backend/src/models/chat.py`
- [x] T019 [US2] Implement ingestion script to index Markdown files in `backend/src/scripts/ingest.py`
- [x] T020 [US2] Implement Chat Service logic (Query -> Embed -> Search -> Answer) in `backend/src/agents/rag.py`
- [x] T021 [US2] Implement `/api/v1/chat` endpoint in `backend/src/api/routes/chat.py` matching `contracts/rag-api.yaml`

### Frontend Implementation
- [x] T022 [P] [US2] Create `ChatWidget` React component in `website/src/components/ChatWidget.tsx`
- [x] T023 [US2] Integrate `ChatWidget` into `website/src/theme/Layout.js` (swizzled) or root provider

**Checkpoint**: Chatbot is functional and integrated.

---

## Phase 5: User Story 3 - Researcher Verifies Citations (Priority: P2)

**Goal**: Ensure academic rigor with valid APA citations and PDF export capability.

**Independent Test**: Check `references.bib` has entries, verify PDF output contains bibliography.

### Implementation for User Story 3

- [ ] T024 [US3] Populate `website/references.bib` with initial 15+ sources (BibTeX format)
- [ ] T025 [US3] Add citation keys (e.g., `[@li2024]`) to `website/docs/01-foundations.md` and `02-humanoids.md`
- [ ] T026 [US3] Create a "Bibliography" page in `website/docs/references.md` that renders the full list
- [ ] T027 [US3] Configure PDF export styling (print media queries) in `website/src/css/print.css`
- [x] T028 [US3] Create script/instruction for PDF generation (e.g., using browser print-to-pdf)

**Checkpoint**: Content is cited and exportable.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [x] T029 [P] Add Remaining Content Chapters (Perception, Control, Simulation) in `website/docs/`
- [x] T030 Optimize RAG prompt system instructions in `backend/src/agents/rag.py`
- [x] T031 Add Rate Limiting to FastAPI in `backend/src/core/security.py`
- [x] T032 Validate all links and citations

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies.
- **Foundational (Phase 2)**: Depends on Setup.
- **User Story 1 (Content)**: Depends on Foundational (Theme/Config).
- **User Story 2 (Chat)**: Depends on Foundational (Backend Core). Can run parallel with US1 content writing.
- **User Story 3 (Citations)**: Depends on US1 (Content existence).

### User Story Dependencies

- **US1 (Content)**: Independent.
- **US2 (Chat)**: Independent of Content specifics, but needs Markdown files to ingest (can use placeholders initially).
- **US3 (Citations)**: Dependent on Content (US1) to place citations.

---

## Implementation Strategy

### MVP First (User Story 1 + 2 Lite)

1. Complete Setup + Foundational.
2. Implement US1 (Site + Theme + 2 Chapters).
3. Implement US2 (Basic Chat backend + Widget).
4. **Validate**: Deploy Site, Chat works with 2 chapters.

### Incremental Delivery

1. Add remaining chapters (Phase 6 task).
2. Re-ingest content for Chat (US2 update).
3. Add Citations (US3) to all chapters.
4. Final PDF Polish.
