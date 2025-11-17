from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from datetime import datetime
from app import db
from app.models.transaction import Transaction
from app.forms.transaction import TransactionForm, TransactionFilterForm

transactions_bp = Blueprint('transactions', __name__)

@transactions_bp.route('/')
@login_required
def list_transactions():
    page = request.args.get('page', 1, type=int)
    per_page = 10
    
    # Get filter parameters
    category = request.args.get('category')
    transaction_type = request.args.get('transaction_type')
    date_from = request.args.get('date_from')
    date_to = request.args.get('date_to')
    
    # Base query
    query = Transaction.query.filter_by(user_id=current_user.id)
    
    # Apply filters
    if category and category != '':
        query = query.filter_by(category=category)
    
    if transaction_type and transaction_type != '':
        if transaction_type == 'income':
            query = query.filter(Transaction.amount > 0)
        else:
            query = query.filter(Transaction.amount < 0)
    
    if date_from:
        date_from = datetime.strptime(date_from, '%Y-%m-%d')
        query = query.filter(Transaction.date >= date_from)
    
    if date_to:
        date_to = datetime.strptime(date_to, '%Y-%m-%d')
        query = query.filter(Transaction.date <= date_to)
    
    # Order by date (newest first)
    query = query.order_by(Transaction.date.desc())
    
    # Paginate
    transactions = query.paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    # Create filter form
    filter_form = TransactionFilterForm(data=request.args)
    
    return render_template('transactions/list.html', 
                         transactions=transactions, 
                         filter_form=filter_form)

@transactions_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add_transaction():
    form = TransactionForm()
    
    if form.validate_on_submit():
        # Convert amount based on transaction type
        amount = form.amount.data
        if form.transaction_type.data == 'expense':
            amount = -abs(amount)
        
        transaction = Transaction(
            amount=amount,
            description=form.description.data,
            category=form.category.data,
            date=form.date.data,
            user_id=current_user.id
        )
        
        db.session.add(transaction)
        db.session.commit()
        
        flash('Transaction added successfully!', 'success')
        return redirect(url_for('transactions.list_transactions'))
    
    # Set default date to today
    if not form.date.data:
        form.date.data = datetime.utcnow().date()
    
    return render_template('transactions/add.html', form=form)

@transactions_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_transaction(id):
    transaction = Transaction.query.filter_by(id=id, user_id=current_user.id).first_or_404()
    
    form = TransactionForm(obj=transaction)
    
    # Set transaction type based on amount
    if transaction.amount < 0:
        form.transaction_type.data = 'expense'
        form.amount.data = abs(transaction.amount)
    else:
        form.transaction_type.data = 'income'
        form.amount.data = transaction.amount
    
    if form.validate_on_submit():
        # Convert amount based on transaction type
        amount = form.amount.data
        if form.transaction_type.data == 'expense':
            amount = -abs(amount)
        
        transaction.amount = amount
        transaction.description = form.description.data
        transaction.category = form.category.data
        transaction.date = form.date.data
        
        db.session.commit()
        
        flash('Transaction updated successfully!', 'success')
        return redirect(url_for('transactions.list_transactions'))
    
    return render_template('transactions/edit.html', form=form, transaction=transaction)

@transactions_bp.route('/delete/<int:id>', methods=['POST'])
@login_required
def delete_transaction(id):
    transaction = Transaction.query.filter_by(id=id, user_id=current_user.id).first_or_404()
    
    db.session.delete(transaction)
    db.session.commit()
    
    flash('Transaction deleted successfully!', 'success')
    return redirect(url_for('transactions.list_transactions'))

@transactions_bp.route('/view/<int:id>')
@login_required
def view_transaction(id):
    transaction = Transaction.query.filter_by(id=id, user_id=current_user.id).first_or_404()
    return render_template('transactions/view.html', transaction=transaction)
