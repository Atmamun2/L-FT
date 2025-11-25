import os
import sys
from pathlib import Path

# Get the project root directory (one level up from config/)
project_root = Path(__file__).parent.parent

# Add the project root to the Python path
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

# Load environment variables
from dotenv import load_dotenv
env_path = project_root / '.env'
if env_path.exists():
    load_dotenv(env_path)

# Import and create the Flask app
from config import create_app
application = create_app(os.getenv('FLASK_CONFIG', 'default'))