#!/usr/bin/env python
"""
Deployment script for PythonAnywhere
Run this script after uploading your code to PythonAnywhere to set up the database
"""

import os
import sys
from pathlib import Path

# Add the project directory to the Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Set environment variables
os.environ['FLASK_CONFIG'] = 'pythonanywhere'
os.environ['FLASK_ENV'] = 'production'

from app import create_app, db
from app.models.user import User
from app.models.transaction import Transaction

def deploy():
    """Run deployment tasks."""
    app = create_app('pythonanywhere')
    
    with app.app_context():
        # Create database tables
        print("Creating database tables...")
        db.create_all()
        
        # Check if admin user exists
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            print("Creating admin user...")
            admin = User(
                username='admin',
                email='admin@example.com',
                first_name='Admin',
                last_name='User',
                is_admin=True
            )
            admin.set_password('admin123')  # Change this password!
            db.session.add(admin)
            db.session.commit()
            print("Admin user created. Please change the default password!")
        
        print("Deployment completed successfully!")

if __name__ == '__main__':
    deploy()
