import os
import sqlite3
from datetime import datetime, timedelta
import random
from werkzeug.security import generate_password_hash

# Get the directory where the database file will be stored
basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(basedir, 'financial_transactions.db')

# Delete the database file if it exists
if os.path.exists(db_path):
    os.remove(db_path)

# Connect to the SQLite database (this will create a new database file)
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Create tables
print("Creating database tables...")

# Users table
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    email TEXT UNIQUE,
    password_hash TEXT NOT NULL,
    first_name TEXT,
    last_name TEXT,
    is_admin BOOLEAN DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP,
    house_id INTEGER
)
''')

# Houses table
cursor.execute('''
CREATE TABLE IF NOT EXISTS houses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    founder_id INTEGER,
    is_active BOOLEAN DEFAULT 1,
    motto TEXT,
    rules TEXT,
    last_merge_date TIMESTAMP,
    FOREIGN KEY (founder_id) REFERENCES users (id)
)
''')

# Transactions table
cursor.execute('''
CREATE TABLE IF NOT EXISTS transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    amount DECIMAL(10, 2) NOT NULL,
    description TEXT,
    category TEXT NOT NULL,
    date TIMESTAMP NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    user_id INTEGER NOT NULL,
    house_id INTEGER,
    FOREIGN KEY (user_id) REFERENCES users (id),
    FOREIGN KEY (house_id) REFERENCES houses (id)
)
''')

# Create indexes for better query performance
cursor.execute('CREATE INDEX IF NOT EXISTS idx_transactions_user_id ON transactions(user_id)')
cursor.execute('CREATE INDEX IF NOT EXISTS idx_transactions_date ON transactions(date)')
cursor.execute('CREATE INDEX IF NOT EXISTS idx_transactions_category ON transactions(category)')
cursor.execute('CREATE INDEX IF NOT EXISTS idx_users_house_id ON users(house_id)')

# Insert sample data
print("Inserting sample data...")

# Insert a default admin user
admin_password = 'admin123'
hashed_password = generate_password_hash(admin_password)
cursor.execute('''
INSERT INTO users (username, email, password_hash, first_name, last_name, is_admin)
VALUES (?, ?, ?, ?, ?, ?)
''', ('admin', 'admin@example.com', hashed_password, 'Admin', 'User', 1))

# Insert a regular user
user_password = 'user123'
hashed_user_password = generate_password_hash(user_password)
cursor.execute('''
INSERT INTO users (username, email, password_hash, first_name, last_name)
VALUES (?, ?, ?, ?, ?)
''', ('john_doe', 'john@example.com', hashed_user_password, 'John', 'Doe'))

# Get the user IDs
admin_id = cursor.lastrowid - 1  # First inserted user is admin
user_id = cursor.lastrowid  # Second inserted user is regular user

# Insert a sample house
cursor.execute('''
INSERT INTO houses (name, description, founder_id, motto, rules)
VALUES (?, ?, ?, ?, ?)
''', ('Smith Family', 'Smith family household', admin_id, 'Family First', '1. Respect each other\n2. No shoes in the house\n3. Clean up after yourself'))

house_id = cursor.lastrowid

# Update admin user to be part of the house
cursor.execute('UPDATE users SET house_id = ? WHERE id = ?', (house_id, admin_id))
cursor.execute('UPDATE users SET house_id = ? WHERE id = ?', (house_id, user_id))

# Sample transaction categories
expense_categories = [
    'Groceries', 'Dining Out', 'Transportation', 'Housing', 'Utilities', 
    'Healthcare', 'Entertainment', 'Shopping', 'Education', 'Gifts', 'Travel'
]

income_categories = [
    'Salary', 'Freelance', 'Investments', 'Gifts', 'Rental Income', 'Bonus'
]

# Generate sample transactions
def random_date(start_date, end_date):
    time_between_dates = end_date - start_date
    days_between_dates = time_between_dates.days
    random_number_of_days = random.randrange(days_between_dates)
    return start_date + timedelta(days=random_number_of_days)

start_date = datetime.now() - timedelta(days=365)
end_date = datetime.now()

# Insert sample transactions
for i in range(100):
    is_expense = random.choice([True, False])
    amount = round(random.uniform(5, 500), 2)
    if is_expense:
        amount = -amount
        category = random.choice(expense_categories)
    else:
        category = random.choice(income_categories)
    
    description = f"Transaction {i+1}" if i % 5 != 0 else None
    date = random_date(start_date, end_date)
    
    cursor.execute('''
    INSERT INTO transactions (amount, description, category, date, user_id, house_id)
    VALUES (?, ?, ?, ?, ?, ?)
    ''', (amount, description, category, date, random.choice([admin_id, user_id]), house_id))

# Commit changes and close the connection
conn.commit()
conn.close()

print(f"Database initialized successfully at {db_path}")
print(f"Admin credentials - Username: admin, Password: {admin_password}")
print(f"User credentials - Username: john_doe, Password: {user_password}")
