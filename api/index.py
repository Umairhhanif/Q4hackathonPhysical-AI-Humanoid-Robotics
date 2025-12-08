import sys
import os

# Add backend directory to sys.path so 'src' module can be found
sys.path.append(os.path.join(os.path.dirname(__file__), '../backend'))

from src.api.main import app
