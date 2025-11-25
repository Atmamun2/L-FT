from flask import Flask, render_template
import os
from pathlib import Path
from .extensions import db, login_manager, mail, migrate, csrf, limiter, cache, babel

def create_app(config_name='default'):
    """Application factory function."""
    app = Flask(__name__)
    
    # Import config based on environment
    if config_name == 'production':
        from config import ProductionConfig as Config
    elif config_name == 'testing':
        from config import TestingConfig as Config
    elif config_name == 'pythonanywhere':
        from config import PythonAnywhereConfig as Config
    else:
        from config import DevelopmentConfig as Config
    
    app.config.from_object(Config)

    # Initialize extensions
    from .extensions import init_extensions
    init_extensions(app)

    # Initialize logger
    from .utils.logger import init_app as init_logger
    init_logger(app)
    app.logger.info(f'Starting application with {config_name} config.')

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

    # Register global error handlers
    @app.errorhandler(404)
    def not_found_error(error):
        app.logger.warning(f'404 Not Found: {error}')
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def internal_error(error):
        app.logger.error(f'500 Internal Server Error: {error}', exc_info=True)
        db.session.rollback()
        return render_template('errors/500.html'), 500

    @app.shell_context_processor
    def make_shell_context():
        # Lazy import models for shell context
        from .models.user import User
        from .models.transaction import Transaction
        return {'db': db, 'User': User, 'Transaction': Transaction}

    return app
