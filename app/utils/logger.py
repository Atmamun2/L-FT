import logging
import os
from logging.handlers import RotatingFileHandler

def init_app(app):
    """Initialize logging for the application."""
    # Clear existing handlers to avoid duplicates
    for handler in app.logger.handlers[:]:
        app.logger.removeHandler(handler)

    if not app.debug and not app.testing:
        logs_dir = os.path.join(app.root_path, '../logs')
        os.makedirs(logs_dir, exist_ok=True)
        file_handler = RotatingFileHandler(
            os.path.join(logs_dir, 'app.log'),
            maxBytes=10240,
            backupCount=10
        )
        formatter = logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        )
        file_handler.setFormatter(formatter)
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)

    console_handler = logging.StreamHandler()
    console_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(console_formatter)
    app.logger.addHandler(console_handler)
    
    app.logger.setLevel(logging.DEBUG if app.debug else logging.INFO)
    app.logger.info('Logger initialized')

def log_error(message, exc_info=False):
    """Logs an error message."""
    from flask import current_app
    current_app.logger.error(message, exc_info=exc_info)