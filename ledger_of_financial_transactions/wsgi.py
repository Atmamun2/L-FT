import os
import sys
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Add your project directory to the Python path
project_root = os.path.dirname(os.path.abspath(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Import the application factory
from app import create_app

# Create application instance
application = create_app(os.getenv('FLASK_ENV') or 'production')

if __name__ == '__main__':
    # This block is used for running the application directly
    # In production, Gunicorn will import this file and use the 'application' variable
    port = int(os.environ.get('PORT', 5000))
    application.run(host='0.0.0.0', port=port)
