# Financial Transactions Ledger

A Flask-based web application for managing financial transactions with user authentication and reporting features.

## Features

- User authentication (login, registration, password reset)
- Transaction management (CRUD operations)
- Financial reporting and analytics
- Responsive design
- Secure password hashing
- CSRF protection
- Rate limiting
- Email notifications

## Prerequisites

- Python 3.9+
- pip (Python package manager)
- Virtual environment (recommended)

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd ledger_of_financial_transactions
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. Initialize the database:
   ```bash
   flask db upgrade
   ```

## Running the Application

### Development Mode
```bash
export FLASK_APP=wsgi.py
export FLASK_ENV=development
flask run
```

### Production Mode
```bash
gunicorn wsgi:application
```

## Deployment

### Heroku

1. Install the Heroku CLI and login:
   ```bash
   heroku login
   ```

2. Create a new Heroku app:
   ```bash
   heroku create your-app-name
   ```

3. Set environment variables:
   ```bash
   heroku config:set FLASK_ENV=production
   heroku config:set SECRET_KEY=your-secret-key
   # Set other environment variables
   ```

4. Deploy the application:
   ```bash
   git push heroku main
   ```

### Docker

1. Build the Docker image:
   ```bash
   docker build -t financial-ledger .
   ```

2. Run the container:
   ```bash
   docker run -d -p 5000:5000 --name ledger-app financial-ledger
   ```

## Environment Variables

See `.env.example` for a list of required environment variables.

## License

[MIT License](LICENSE)
