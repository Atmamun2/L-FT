import os
import sys
from pathlib import Path

# Get the directory containing the current script
current_dir = Path(__file__).parent

# Add the project directory to the Python path
if str(current_dir) not in sys.path:
    sys.path.insert(0, str(current_dir))

# Load environment variables
from dotenv import load_dotenv
dotenv_path = current_dir / '.env'
if dotenv_path.exists():
    load_dotenv(dotenv_path)

# Import and create the Flask app
from app import create_app
application = create_app(os.getenv('FLASK_CONFIG', 'default'))