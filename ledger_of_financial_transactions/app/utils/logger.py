"""
Logging configuration for the application.
"""
import logging
import os
from logging.handlers import RotatingFileHandler
from flask import current_app, request
import json
from datetime import datetime

class JSONFormatter(logging.Formatter):
    """Custom formatter that outputs logs in JSON format."""
    
    def format(self, record):
        log_record = {
            'timestamp': datetime.utcnow().isoformat(),
            'level': record.levelname,
            'message': record.getMessage(),
            'module': record.module,
            'function': record.funcName,
            'line': record.lineno,
            'logger': record.name,
        }
        
        # Add request-specific information if available
        if has_request_context():
            log_record.update({
                'url': request.url,
                'method': request.method,
                'endpoint': request.endpoint,
                'ip': request.remote_addr,
                'user_agent': request.user_agent.string,
            })
            
            # Add user information if available
            if current_user.is_authenticated:
                log_record['user_id'] = current_user.id
                log_record['username'] = current_user.username
        
        # Add exception information if present
        if record.exc_info:
            log_record['exception'] = self.formatException(record.exc_info)
        
        return json.dumps(log_record, ensure_ascii=False)

def has_request_context():
    """Check if we're in a request context."""
    try:
        from flask import has_request_context as flask_has_request_context
        return flask_has_request_context()
    except RuntimeError:
        return False

def init_app(app):
    """Initialize logging for the application."""
    # Disable the default Flask logger
    app.logger.handlers.clear()
    
    # Set the log level from config or default to INFO
    log_level = app.config.get('LOG_LEVEL', 'INFO')
    app.logger.setLevel(getattr(logging, log_level.upper(), logging.INFO))
    
    # Create logs directory if it doesn't exist
    logs_dir = os.path.join(app.root_path, 'logs')
    os.makedirs(logs_dir, exist_ok=True)
    
    # File handler for application logs
    file_handler = RotatingFileHandler(
        os.path.join(logs_dir, 'app.log'),
        maxBytes=1024 * 1024 * 10,  # 10MB per file
        backupCount=10,
        encoding='utf-8'
    )
    
    # Set formatter
    if app.config.get('JSON_LOGGING', False):
        formatter = JSONFormatter()
    else:
        formatter = logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        )
    
    file_handler.setFormatter(formatter)
    
    # Add handlers to the application logger
    app.logger.addHandler(file_handler)
    
    # Also log to console in development
    if app.debug:
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        app.logger.addHandler(console_handler)
    
    # Log application startup
    app.logger.info('Application startup')
    
    # Configure SQLAlchemy logging if needed
    if app.config.get('SQLALCHEMY_ECHO'):
        logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)
        logging.getLogger('sqlalchemy.pool').setLevel(logging.DEBUG)
    
    # Set up other loggers
    for logger_name in ['werkzeug', 'flask', 'sqlalchemy']:
        logger = logging.getLogger(logger_name)
        logger.setLevel(logging.WARNING)  # Reduce noise from these loggers
        logger.addHandler(file_handler)
    
    return app.logger

# Create a module-level logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Prevent double logging in case the logger is imported multiple times
if not logger.handlers:
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    ))
    logger.addHandler(handler)
