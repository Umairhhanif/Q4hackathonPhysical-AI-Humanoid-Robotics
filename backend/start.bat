@echo off
REM Startup script for Physical AI RAG Chatbot Backend
echo Starting Physical AI RAG Chatbot Backend...

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Start the server
python run.py
