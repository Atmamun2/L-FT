from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
from flask_caching import Cache
from flask_babel import Babel

# Initialize extensions for Flask 3.0 compatibility
db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()
csrf = CSRFProtect()
babel = Babel()

# Make flask_limiter optional
try:
    from flask_limiter import Limiter
    from flask_limiter.util import get_remote_address
    limiter = Limiter(key_func=get_remote_address, default_limits=["200 per day", "50 per hour"])
except ImportError:
    # Create a dummy limiter if flask_limiter is not available
    class DummyLimiter:
        def __getattr__(self, name):
            return self
        
        def __call__(self, *args, **kwargs):
            return self
            
        def limit(self, *args, **kwargs):
            def decorator(f):
                return f
            return decorator
    
    limiter = DummyLimiter()

def init_extensions(app):
    """Initialize all extensions with the Flask app."""
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    csrf.init_app(app)
    babel.init_app(app)
