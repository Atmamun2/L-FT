from pathlib import Path
import os
from dotenv import load_dotenv

# Load environment variables
env_path = Path(__file__).parent / '.env'
if env_path.exists():
    load_dotenv(env_path)

from .settings import *

# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'pythonanywhere': PythonAnywhereConfig,
    'default': DevelopmentConfig
}

# Export the create_app function from the app package
def create_app(config_name='default'):
    from app import create_app as _create_app
    return _create_app(config_name)
