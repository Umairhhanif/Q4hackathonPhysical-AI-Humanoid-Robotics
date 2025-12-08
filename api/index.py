import os
import sys

# Add the project root and backend directory to sys.path
# This allows importing 'src' as if we were running from 'backend/'
current_dir = os.path.dirname(os.path.abspath(__file__))
# api/ -> root -> backend
project_root = os.path.dirname(current_dir)
backend_dir = os.path.join(project_root, 'backend')

sys.path.append(project_root)
sys.path.append(backend_dir)

# Now we can import the genuine FastAPI app
from src.api.main import app

# Vercel needs a variable named 'app' or 'handler'
handler = app
