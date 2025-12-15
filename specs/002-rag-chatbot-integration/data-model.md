# Data Model: RAG Chatbot Integration

## Entities

### DocumentChunk
Represents a segment of the book content stored in the vector database.

| Field | Type | Description |
|-------|------|-------------|
| `id` | UUID | Unique identifier for the chunk (generated deterministically from content/path). |
| `content` | String | The actual text content of the chunk. |
| `embedding` | List[Float] | 1536-dim vector representation. |
| `source_file` | String | Path to the source markdown file (e.g., `docs/intro.md`). |
| `header_path` | String | Hierarchical path (e.g., "Introduction > Why Physical AI"). |
| `token_count` | Integer | Number of tokens in the chunk. |

### ChatMessage
Represents a single message in a conversation.

| Field | Type | Description |
|-------|------|-------------|
| `role` | Enum | `user` or `assistant`. |
| `content` | String | The text of the message. |
| `timestamp` | DateTime | When the message was sent. |

### ChatRequest
Payload sent from frontend to backend.

| Field | Type | Description |
|-------|------|-------------|
| `query` | String | The user's question. |
| `selected_text` | String (Optional) | Text highlighted by the user in the book. |
| `history` | List[ChatMessage] | Previous conversation context (last N messages). |

### ChatResponse
Payload returned to frontend.

| Field | Type | Description |
|-------|------|-------------|
| `answer` | String | The generated response (streamed). |
| `sources` | List[SourceReference] | Citations used in the answer. |

### InteractionLog (Postgres)
Persistent record of chat interactions for analytics.

| Field | Type | Description |
|-------|------|-------------|
| `id` | UUID | Unique ID. |
| `timestamp` | DateTime | Creation time. |
| `user_query` | String | The user's input. |
| `bot_response` | String | The final generated response. |
| `tokens_input` | Integer | Tokens used in prompt. |
| `tokens_output` | Integer | Tokens generated. |
| `latency_ms` | Integer | Total response time. |
| `successful` | Boolean | Whether the request completed without error. |
