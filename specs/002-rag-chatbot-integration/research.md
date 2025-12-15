# Research: RAG Chatbot Integration

**Decision**: Decisions and research findings for the RAG Chatbot Integration.

## 1. Embedding Model Choice

**Decision**: Use **OpenAI `text-embedding-3-small`**.

**Rationale**:
- **Performance/Cost**: High performance at a very low cost. Standard for RAG applications.
- **Compatibility**: Natively supported by almost all RAG frameworks, including Qdrant and OpenAI Agent tools.
- **Dimension**: 1536 dimensions, compatible with Qdrant's standard configuration.

**Alternatives Considered**:
- **Google `text-embedding-004`**: Good alternative if going all-in on Google, but `text-embedding-3-small` is the de facto standard for general RAG setups and ensures compatibility if the user swaps the LLM provider. Given the "OpenAI ChatKit" requirement, keeping the embedding model in the same ecosystem (or the standard compatible one) simplifies the stack.
- **HuggingFace (local)**: Rejected to avoid complexity in deployment and resource usage on Vercel/cloud functions.

## 2. Chunking Strategy

**Decision**: **Recursive Character Text Splitter** with markdown awareness.

**Rationale**:
- **Structure Preservation**: The book is in Markdown. We need to split by headers (`#`, `##`, `###`) to preserve semantic structure.
- **Context**: Code blocks must be kept intact where possible.
- **Size**: Target chunk size of ~1000 tokens with 200 token overlap to ensure context continuity across boundaries.

**Alternatives Considered**:
- **Fixed-size**: Too crude for technical documentation; risks splitting code blocks or sentences.
- **Semantic Chunking**: Higher complexity/latency to generate; recursive character splitting is sufficient for a 2-week timeline.

## 3. Vector Schema Design (Qdrant)

**Decision**: Single Collection `book_content` with payload based filtering.

**Schema**:
- **Vector**: 1536 dimensions (for `text-embedding-3-small`).
- **Distance**: Cosine.
- **Payload**:
    - `source_file` (keyword): Path to the markdown file.
    - `chapter` (keyword): Extracted from directory or metadata.
    - `content` (text): The actual chunk text.
    - `header_path` (text): Breadcrumb context (e.g., "Chapter 1 > Section 2").

**Rationale**: Simple schema allows for easy filtering by chapter or file if needed later. Storing content in payload avoids a secondary database lookup for retrieval.

## 4. Retrieval Heuristics

**Decision**: **Hybrid Search** (Dense Vector + Keyword) if possible, otherwise standard Dense Vector with a "top-k" of 5.

**Rationale**:
- **Top-K**: 5 chunks usually provide enough context without overflowing the context window.
- **Score Threshold**: 0.7 to filter out irrelevant noise.

## 5. FastAPI Route Design

**Decision**:
- `POST /chat`: Accepts `{ query: str, selected_text: Optional[str], history: List[Message] }`. Returns streaming response.
- `POST /ingest`: Protected endpoint (API Key) to trigger re-indexing of the `docs/` folder.

**Rationale**: Simple, RESTful design. Streaming is critical for UX.

## 6. Selected Text Handling

**Decision**: Append `selected_text` to the system prompt or user query with high emphasis.

**Mechanism**:
- If `selected_text` is present:
    1.  Perform retrieval using the `selected_text` + `query` as the search vector (to find surrounding context).
    2.  Inject `selected_text` into the prompt explicitly: "User has selected this text: \"{selected_text}\". Focus your answer on this context."

**Rationale**: This ensures the model knows exactly what the user is pointing at, while still retrieving related concepts.

## 7. Model Selection (LLM)

**Decision**: **Google Gemini 1.5 Flash** (via OpenAI-compatible API or Google GenAI SDK).

**Rationale**:
- **User Request**: Explicitly requested "google gemini model".
- **Performance**: 1.5 Flash is fast and cost-effective, ideal for a chatbot.
- **Context Window**: Large context window allows for including more retrieved chunks if necessary.

## 8. Orchestration

**Decision**: **OpenAI ChatKit / Agents (Python)** or a lightweight wrapper around the Chat Completions API if the full "Agent" toolkit is overkill.

**Clarification**: The user requested "OpenAI ChatKit". This usually refers to the Vercel AI SDK (frontend) or the OpenAI Assistants API. Given the Python backend requirement, we will use the **OpenAI Python SDK** (which supports Gemini via compatible endpoints if configured, or we use standard Google SDK and wrap it to look like an "agent" to the frontend).
*Refinement*: To strictly follow "OpenAI ChatKit for orchestration" AND "Google Gemini model": We will use the **Vercel AI SDK** on the frontend (standard for Docusaurus/React chat) and on the backend, we'll use the **Google Generative AI SDK** wrapped in a Vercel AI SDK compatible stream (using `ai` package in Python or just standard streaming response).
*Correction*: The user said "OpenAI ChatKit" in the context of "Orchestration". This might refer to a specific pattern. I will assume a standard RAG flow: Retrieve -> Augment -> Generate, orchestrated by a simple Python service, exposed to the frontend.

**Dependencies**:
- `fastapi`
- `qdrant-client`
- `google-generativeai` (for Gemini)
- `openai` (for embeddings, if using OpenAI embeddings)
- `langchain-text-splitters` (for chunking)
