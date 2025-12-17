---
title: Physical AI Chatbot Backend
emoji: 🤖
colorFrom: blue
colorTo: purple
sdk: docker
app_port: 7860
license: mit
---

# Physical AI & Humanoid Robotics Chatbot - Backend

This is the backend API for the Physical AI RAG Chatbot.

## 🚀 Features
- **FastAPI**: High-performance async API
- **RAG Pipeline**: Retrieves context from the "Physical AI & Humanoid Robotics" book
- **Qdrant**: Vector database for efficient similarity search
- **Google Gemini / Cohere**: LLM and Embeddings integration
- **Streaming**: Real-time response streaming

## 🛠️ Usage
This space hosts the API compliant with the frontend application.

### Endpoints
- `POST /api/v1/chat`: Chat endpoint (Streaming response)
