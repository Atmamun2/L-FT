import os
from pathlib import Path
from dotenv import load_dotenv

# Get the base directory
basedir = Path(__file__).parent

# Load environment variables
env_path = basedir / '.env'
if env_path.exists():
    load_dotenv(env_path)

class Config:
    # App settings
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key-123'
    FLASK_ENV = os.environ.get('FLASK_ENV', 'production')
    DEBUG = os.environ.get('FLASK_DEBUG', '0').lower() in ['1', 'true', 't', 'y', 'yes']
    
    # Database
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        f'sqlite:///{(basedir / "instance" / "app.db").as_posix()}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = DEBUG

    # Security
    SESSION_COOKIE_SECURE = True
    REMEMBER_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_HTTPONLY = True

    # Email
    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.googlemail.com')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', '587'))
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'true').lower() in ['true', 'on', '1']
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME', '')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD', '')
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER', 'noreply@example.com')

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_ECHO = True
    SESSION_COOKIE_SECURE = False
    REMEMBER_COOKIE_SECURE = False

class TestingConfig(Config):
    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'

class ProductionConfig(Config):
    pass

class PythonAnywhereConfig(Config):
    DEBUG = False
    # PythonAnywhere MySQL database
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}'.format(
            username=os.environ.get('DB_USERNAME', 'Atmamun2$default'),
            password=os.environ.get('DB_PASSWORD', ''),
            hostname=os.environ.get('DB_HOSTNAME', 'Atmamun2.mysql.pythonanywhere-services.com'),
            databasename=os.environ.get('DB_NAME', 'Atmamun2$default')
        )

# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'pythonanywhere': PythonAnywhereConfig,
    'default': DevelopmentConfig
}