from flask import Blueprint, render_template, redirect, url_for
from flask_login import current_user, login_required
from datetime import datetime, timedelta
from app.models.transaction import Transaction
from app.models.user import User

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    return render_template('index.html')

@main_bp.route('/dashboard')
@login_required
def dashboard():
    # Calculate financial data
    now = datetime.utcnow()
    start_of_month = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    
    # Get all user transactions
    user_transactions = Transaction.query.filter_by(user_id=current_user.id).all()
    
    # Calculate total balance
    balance = sum(t.amount for t in user_transactions)
    
    # Calculate monthly income and expenses
    monthly_transactions = Transaction.query.filter(
        Transaction.user_id == current_user.id,
        Transaction.date >= start_of_month
    ).all()
    
    monthly_income = sum(t.amount for t in monthly_transactions if t.amount > 0)
    monthly_expenses = abs(sum(t.amount for t in monthly_transactions if t.amount < 0))
    
    # Get recent transactions (last 10)
    recent_transactions = Transaction.query.filter_by(user_id=current_user.id)\
        .order_by(Transaction.date.desc())\
        .limit(10)\
        .all()
    
    return render_template('dashboard.html', 
                         balance=balance,
                         monthly_income=monthly_income,
                         monthly_expenses=monthly_expenses,
                         recent_transactions=recent_transactions)
