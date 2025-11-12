import os
from flask import Flask, current_app, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user
from flask_mail import Mail
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_caching import Cache
from flask_babel import Babel, lazy_gettext as _l
from config import config

# Initialize extensions
db = SQLAlchemy()
login_manager = LoginManager()
mail = Mail()
migrate = Migrate()
csrf = CSRFProtect()
cache = Cache()
babel = Babel()

# Rate limiting
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="memory://",
)

# Configure login manager
login_manager.login_view = 'auth.login'
login_manager.login_message = _l('Please log in to access this page.')
login_manager.login_message_category = 'info'


def create_app(config_name='default'):
    """Application factory function to create and configure the Flask app."""
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    
    # Initialize logger first
    from .utils.logger import init_app as init_logger
    logger = init_logger(app)
    
    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    migrate.init_app(app, db)
    csrf.init_app(app)
    limiter.init_app(app)
    cache.init_app(app)
    babel.init_app(app)
    
    # Log application startup
    app.logger.info('Application starting up')
    app.logger.info(f'Environment: {config_name}')
    app.logger.info(f'Debug mode: {app.debug}')
    app.logger.info(f'Database: {app.config["SQLALCHEMY_DATABASE_URI"]}')
    
    # Register blueprints
    from .routes.main import main_bp
    from .routes.auth import auth_bp
    from .routes.transactions import transactions_bp
    from .routes.api import api_bp
    from .routes.admin import admin_bp
    from .routes.errors import errors_bp
    
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(transactions_bp, url_prefix='/transactions')
    app.register_blueprint(api_bp, url_prefix='/api/v1')
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(errors_bp)
    
    # Register context processors
    from .utils.context_processors import inject_now, inject_user, format_currency
    
    app.context_processor(inject_now)
    app.context_processor(inject_user)
    
    # Register template filters
    app.template_filter('currency')(format_currency)
    
    # Configure error handlers
    from .utils.errors import page_not_found, internal_server_error, forbidden, handle_exception
    
    app.register_error_handler(404, page_not_found)
    app.register_error_handler(403, forbidden)
    app.register_error_handler(500, internal_server_error)
    app.register_error_handler(Exception, handle_exception)
    
    # Shell context
    @app.shell_context_processor
    def make_shell_context():
        from .models import User, Transaction, House, Category, Budget
        return {
            'db': db,
            'User': User,
            'Transaction': Transaction,
            'House': House,
            'Category': Category,
            'Budget': Budget
        }
    
    # Database initialization
    @app.before_first_request
    def initialize_database():
        with app.app_context():
            # Create database tables
            db.create_all()
            
            # Create default admin user if not exists
            from .models import User
            from werkzeug.security import generate_password_hash
            
            admin = User.query.filter_by(username='admin').first()
            if not admin and app.config.get('FLASK_ENV') != 'production':
                admin = User(
                    username='admin',
                    email='admin@example.com',
                    password=generate_password_hash('admin123'),
                    first_name='Admin',
                    last_name='User',
                    is_admin=True
                )
                db.session.add(admin)
                db.session.commit()
    
    # Request hooks
    @app.before_request
    def before_request():
        from flask import g, request
        from flask_login import current_user
        
        g.user = current_user
        
        # Update user's last seen time
        if current_user.is_authenticated:
            current_user.ping()
    
    return app
