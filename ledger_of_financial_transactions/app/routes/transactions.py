from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from datetime import datetime
from app import db
from app.models.transaction import Transaction
from app.models.house import House

transactions_bp = Blueprint('transactions', __name__)

@transactions_bp.route('/')
@login_required
def list_transactions():
    page = request.args.get('page', 1, type=int)
    per_page = 10
    
    # Get filter parameters
    category = request.args.get('category')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    # Base query
    query = Transaction.query.filter_by(user_id=current_user.id)
    
    # Apply filters
    if category and category != 'all':
        query = query.filter_by(category=category)
    
    if start_date:
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        query = query.filter(Transaction.date >= start_date)
    
    if end_date:
        end_date = datetime.strptime(end_date, '%Y-%m-%d')
        query = query.filter(Transaction.date <= end_date)
    
    # Execute query with pagination
    transactions = query.order_by(Transaction.date.desc()).paginate(page=page, per_page=per_page)
    
    # Get unique categories for filter dropdown
    categories = db.session.query(Transaction.category).distinct().all()
    categories = [cat[0] for cat in categories]
    
    return render_template('transactions/list.html', 
                         transactions=transactions,
                         categories=categories,
                         current_filters={
                             'category': category,
                             'start_date': start_date.strftime('%Y-%m-%d') if start_date else '',
                             'end_date': end_date.strftime('%Y-%m-%d') if end_date else ''
                         })

@transactions_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add_transaction():
    if request.method == 'POST':
        try:
            amount = float(request.form.get('amount'))
            description = request.form.get('description', '').strip()
            category = request.form.get('category')
            date = datetime.strptime(request.form.get('date'), '%Y-%m-%d')
            
            transaction = Transaction(
                amount=amount,
                description=description,
                category=category,
                date=date,
                user_id=current_user.id,
                house_id=current_user.house_id
            )
            
            db.session.add(transaction)
            db.session.commit()
            
            flash('Transaction added successfully!', 'success')
            return redirect(url_for('transactions.list_transactions'))
            
        except ValueError as e:
            db.session.rollback()
            flash('Invalid input. Please check your entries.', 'error')
    
    return render_template('transactions/add.html')

@transactions_bp.route('/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_transaction(id):
    transaction = Transaction.query.get_or_404(id)
    
    # Ensure the user owns this transaction
    if transaction.user_id != current_user.id and not current_user.is_admin:
        flash('You do not have permission to edit this transaction.', 'error')
        return redirect(url_for('transactions.list_transactions'))
    
    if request.method == 'POST':
        try:
            transaction.amount = float(request.form.get('amount'))
            transaction.description = request.form.get('description', '').strip()
            transaction.category = request.form.get('category')
            transaction.date = datetime.strptime(request.form.get('date'), '%Y-%m-%d')
            
            db.session.commit()
            flash('Transaction updated successfully!', 'success')
            return redirect(url_for('transactions.list_transactions'))
            
        except ValueError as e:
            db.session.rollback()
            flash('Invalid input. Please check your entries.', 'error')
    
    return render_template('transactions/edit.html', transaction=transaction)

@transactions_bp.route('/<int:id>/delete', methods=['POST'])
@login_required
def delete_transaction(id):
    transaction = Transaction.query.get_or_404(id)
    
    # Ensure the user owns this transaction or is an admin
    if transaction.user_id != current_user.id and not current_user.is_admin:
        flash('You do not have permission to delete this transaction.', 'error')
        return redirect(url_for('transactions.list_transactions'))
    
    db.session.delete(transaction)
    db.session.commit()
    
    flash('Transaction deleted successfully!', 'success')
    return redirect(url_for('transactions.list_transactions'))

@transactions_bp.route('/categories')
@login_required
def categories():
    # Get category totals for the current user
    categories = db.session.query(
        Transaction.category,
        db.func.sum(Transaction.amount).label('total')
    ).filter_by(user_id=current_user.id)\
     .group_by(Transaction.category)\
     .order_by(db.desc('total'))\
     .all()
    
    return render_template('transactions/categories.html', categories=categories)
