import sys
import os

# Add backend directory to sys.path so 'src' module can be found
backend_path = os.path.join(os.path.dirname(__file__), '../backend')
sys.path.insert(0, backend_path)

try:
    # Check critical environment variables
    required_env_vars = ['GOOGLE_API_KEY', 'QDRANT_URL', 'QDRANT_API_KEY', 'DATABASE_URL', 'API_SECRET']
    missing_vars = [var for var in required_env_vars if not os.getenv(var)]
    
    if missing_vars:
        raise EnvironmentError(f"Missing required environment variables: {', '.join(missing_vars)}")
    
    from src.api.main import app
    
except Exception as e:
    import traceback
    from fastapi import FastAPI
    from fastapi.responses import JSONResponse
    from fastapi.middleware.cors import CORSMiddleware
    
    app = FastAPI()
    
    # Add CORS for error responses
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    error_details = {
        "error": "Startup Error",
        "message": str(e),
        "traceback": traceback.format_exc(),
        "backend_path": backend_path,
        "sys_path": sys.path[:3],
        "cwd": os.getcwd(),
    }
    
    @app.get("/{path:path}")
    @app.post("/{path:path}")
    async def catch_all(path: str):
        return JSONResponse(content=error_details, status_code=500)

