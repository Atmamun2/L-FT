from app import create_app, db
from app.models.user import User
from werkzeug.security import generate_password_hash

def create_tables():
    app = create_app('development')
    with app.app_context():
        # Create all database tables
        db.create_all()
        
        # Create a test user if it doesn't exist
        if not User.query.filter_by(username='testuser').first():
            user = User(
                username='testuser',
                email='test@example.com',
                password=generate_password_hash('password', method='pbkdf2:sha256')
            )
            db.session.add(user)
            db.session.commit()
            print("Test user created successfully!")
        else:
            print("Test user already exists.")

if __name__ == '__main__':
    create_tables()
