from flask_wtf import FlaskForm
from wtforms import FloatField, TextAreaField, SelectField, DateField, SubmitField
from wtforms.validators import DataRequired, NumberRange, Length, Optional

class TransactionForm(FlaskForm):
    amount = FloatField('Amount', validators=[
        DataRequired(message='Amount is required'),
        NumberRange(min=0.01, message='Amount must be greater than 0')
    ])
    
    description = TextAreaField('Description', validators=[
        Length(max=200, message='Description cannot exceed 200 characters')
    ])
    
    category = SelectField('Category', choices=[
        ('Food & Dining', 'Food & Dining'),
        ('Transportation', 'Transportation'),
        ('Shopping', 'Shopping'),
        ('Entertainment', 'Entertainment'),
        ('Bills & Utilities', 'Bills & Utilities'),
        ('Healthcare', 'Healthcare'),
        ('Education', 'Education'),
        ('Travel', 'Travel'),
        ('Other', 'Other')
    ], validators=[DataRequired(message='Category is required')])
    
    transaction_type = SelectField('Type', choices=[
        ('expense', 'Expense'),
        ('income', 'Income')
    ], validators=[DataRequired(message='Transaction type is required')])
    
    date = DateField('Date', validators=[DataRequired(message='Date is required')])
    
    submit = SubmitField('Save Transaction')

class TransactionFilterForm(FlaskForm):
    category = SelectField('Category', choices=[
        ('', 'All Categories'),
        ('Food & Dining', 'Food & Dining'),
        ('Transportation', 'Transportation'),
        ('Shopping', 'Shopping'),
        ('Entertainment', 'Entertainment'),
        ('Bills & Utilities', 'Bills & Utilities'),
        ('Healthcare', 'Healthcare'),
        ('Education', 'Education'),
        ('Travel', 'Travel'),
        ('Other', 'Other')
    ], validators=[Optional()])
    
    transaction_type = SelectField('Type', choices=[
        ('', 'All Types'),
        ('expense', 'Expense'),
        ('income', 'Income')
    ], validators=[Optional()])
    
    date_from = DateField('From', validators=[Optional()])
    date_to = DateField('To', validators=[Optional()])
    
    submit = SubmitField('Filter')
