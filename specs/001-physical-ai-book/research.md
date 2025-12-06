# Research & Decisions: Physical AI Book

**Feature**: 001-physical-ai-book
**Date**: 2025-12-05

## 1. Docusaurus Theme Implementation
**Decision**: Pure Custom CSS (Neon Theme).
**Rationale**: Provides granular control over the specific "Neon" aesthetic (glow effects, rounded borders) without the overhead or limitations of third-party themes.
**Implementation Details**:
- Use `src/css/custom.css`.
- Override CSS variables: `--ifm-color-primary` (Cyan #00ffea), `--ifm-background-color` (Dark Blue #000028).
- Buttons: `border-radius: 50px`, `box-shadow` for glow.

## 2. Citation Management
**Decision**: Use `rehype-citation` plugin.
**Rationale**: The built-in "remark" support in Docusaurus needs a specific plugin to handle APA style referencing from a BibTeX file correctly. `rehype-citation` is standard for this stack.
**Alternatives Considered**:
- `remark-bibtex`: Older, less flexible.
- Manual HTML links: Hard to maintain, violates "Traceability" principle.

## 3. RAG Chatbot Integration
**Decision**: Custom React Component (`ChatWidget`) in Docusaurus talking to FastAPI Backend.
**Rationale**: Docusaurus is static; the chat needs a dynamic backend. A floating widget component is the standard UI pattern for documentation assistance.
**Architecture**:
- **Frontend**: React Component `ChatWidget` uses `fetch()` to call Backend API.
- **Backend**: FastAPI service exposes `/api/v1/chat`.
- **Auth**: API Key or Rate Limiting on Backend (Public Read Access for MVP).

## 4. Diagrams
**Decision**: draw.io -> SVG.
**Rationale**: SVGs scale perfectly and allow CSS styling/class manipulation if needed for dark mode compatibility (high contrast).

## 5. Animation Strategy
**Decision**: CSS Keyframes.
**Rationale**: Lightweight, no JS bundle size impact (unlike Framer Motion), sufficient for button glows and hover effects.
