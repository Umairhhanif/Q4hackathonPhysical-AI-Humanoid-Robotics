import sys
import os

try:
    # Add backend directory to sys.path so 'src' module can be found
    sys.path.append(os.path.join(os.path.dirname(__file__), '../backend'))
    
    from src.api.main import app
except Exception as e:
    import traceback
    from fastapi import FastAPI
    from fastapi.responses import PlainTextResponse
    
    app = FastAPI()
    
    @app.get("/{path:path}")
    def catch_all(path: str):
        return PlainTextResponse(f"Startup Error:\n{traceback.format_exc()}", status_code=500)
