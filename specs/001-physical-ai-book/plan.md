# Implementation Plan: Physical AI & Humanoid Robotics Book

**Branch**: `001-physical-ai-book` | **Date**: 2025-12-05 | **Spec**: [specs/001-physical-ai-book/spec.md](specs/001-physical-ai-book/spec.md)
**Input**: Feature specification from `/specs/001-physical-ai-book/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Develop a 5,000–7,000 word technical book on Physical AI and Humanoid Robotics using Docusaurus v3, hosted on GitHub Pages. Integrate a RAG-based chatbot (FastAPI + Qdrant + OpenAI) to answer reader queries. The site will feature a custom "Neon" aesthetic (CSS) and adhere to strict academic rigor (APA citations, peer-reviewed sources).

## Technical Context

**Language/Version**: TypeScript 5.x (Docusaurus), Python 3.10+ (Backend), CSS3
**Primary Dependencies**:
- Frontend: Docusaurus v3 (Classic Preset), React 18, rehype-citation (for APA)
- Backend: FastAPI, OpenAI SDK, Qdrant Client, Neon Postgres Driver
**Storage**:
- Vector: Qdrant Cloud (Free Tier)
- Relational: Neon Serverless Postgres (for logs/metadata)
- Content: Markdown files (Git)
**Testing**:
- Frontend: Jest (Unit), Playwright (E2E for site navigation)
- Backend: Pytest
**Target Platform**: GitHub Pages (Static Site), Render/Railway (Backend - *Implied for RAG API hosting*)
**Project Type**: Web application (Static Frontend + API Backend)
**Performance Goals**:
- Site Load: < 1.5s LCP (Static)
- Chat Latency: < 3s for answer generation
**Constraints**:
- Strict APA citation format
- Zero plagiarism
- Mobile responsive design
**Scale/Scope**: ~10 Chapters, ~100MB assets, Low concurrent chat users (initially)

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- **Accuracy**: Verified by Primary Source requirement (Sources stored in Zotero/BibTeX).
- **Clarity**: Readability checks (Flesch-Kincaid) integrated into workflow.
- **Reproducibility**: "Fresh Ubuntu" install test defined in Quickstart.
- **Rigor**: Minimum 20 sources, 60% peer-reviewed (Exceeds 50% constitution minimum).

## Project Structure

### Documentation (this feature)

```text
specs/001-physical-ai-book/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
# Option 2: Web application
backend/
├── src/
│   ├── agents/          # RAG Logic
│   ├── api/             # FastAPI Routes
│   ├── core/            # Config & Utils
│   └── services/        # Qdrant/OpenAI Connectors
└── tests/

website/                 # Docusaurus Root
├── docs/                # Markdown Content (The Book)
├── src/
│   ├── components/      # Custom React Components (ChatWidget)
│   ├── css/             # Custom Neon Theme
│   └── pages/           # Landing Page
├── static/              # Images/Diagrams
└── tests/               # E2E Tests
```

**Structure Decision**: Split structure (Frontend/Backend) to separate static content generation (Docusaurus) from dynamic RAG processing (FastAPI).

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| None | N/A | N/A |
