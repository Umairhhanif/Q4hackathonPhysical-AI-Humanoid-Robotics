# Data Model: Physical AI Book

**Feature**: 001-physical-ai-book
**Date**: 2025-12-05

## Core Entities

### 1. BookChapter (Markdown File)
**Description**: A unit of documentation content.
**Storage**: Git (Filesystem)
**Format**: Markdown + Frontmatter

| Field | Type | Description |
|-------|------|-------------|
| `slug` | string | URL path component (e.g., `/modules/module-1`) |
| `title` | string | Chapter title |
| `sidebar_position` | integer | Order in navigation |
| `content` | markdown | The actual text content |
| `references` | list<string> | Keys to BibTeX citations |

### 2. Citation (Reference)
**Description**: A bibliographic source.
**Storage**: `references.bib` (BibTeX)

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Unique citation key (e.g., `li2024humanoid`) |
| `type` | enum | `article`, `book`, `webpage` |
| `author` | string | Author names |
| `year` | integer | Publication year |
| `title` | string | Title of work |
| `doi` | string | Digital Object Identifier (optional) |
| `url` | string | Source URL |

### 3. VectorEmbedding
**Description**: Indexed chunk of text for RAG.
**Storage**: Qdrant

| Field | Type | Description |
|-------|------|-------------|
| `id` | uuid | Unique Chunk ID |
| `vector` | float[] | 1536-dim vector (OpenAI text-embedding-3-small) |
| `payload.text` | string | Original text content |
| `payload.source` | string | Chapter/Section reference |

### 4. ChatSession (Ephemeral)
**Description**: A user's interaction with the RAG bot.
**Storage**: Neon Postgres (Logs) / In-Memory (Context)

| Field | Type | Description |
|-------|------|-------------|
| `session_id` | uuid | Unique Session ID |
| `user_query` | string | The question asked |
| `bot_response` | string | The generated answer |
| `citations` | list<string> | Sources used for the answer |
| `timestamp` | datetime | Time of query |
