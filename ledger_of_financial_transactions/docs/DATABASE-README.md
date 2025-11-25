# GCD Database Application

A comprehensive database system for the **Generis Citadel Dynasty (GCD)** financial ecosystem. This application provides the complete backend infrastructure for managing family "Houses," financial transactions, governance systems, and multi-generational wealth tracking.

## 🏰 Overview

The GCD database application implements the complete vision of a blockchain-inspired financial ecosystem where:

- **Houses** represent family units with shared financial goals
- **Members** have roles, contribution scores, and voting rights
- **Transactions** are recorded with double-entry accounting
- **Governance** includes veto systems and house mergers
- **Assets** are tracked and valued across generations
- **Audit trails** maintain complete transparency

## 📁 Files Overview

### Core Database Files

- **`gcd_database.py`** - Main database module with all GCD-specific functions
- **`gcd_schema.sql`** - Complete database schema with all tables and relationships
- **`gcd_cli.py`** - Command-line interface for interacting with the database

### Integration Files

- **`database.py`** - Your existing database module (for reference)
- **`schema.sql`** - Your existing schema (for reference)

## 🚀 Quick Start

### 1. Initialize the Database

```bash
cd /Users/atmamun/Programming/SOFT12/L-FT/ledger_of_financial_transactions
python gcd_cli.py
```

Choose option **6** to initialize the database with the GCD schema.

### 2. Seed Example Data

Choose option **7** to populate the database with comprehensive example data including:

- **Anderson Dynasty** house with 5 members
- **Smith Heritage** house (for merge examples)
- Sample assets, transactions, and governance proposals
- Complete audit trail and metrics

### 3. Explore the System

Use the CLI menu to:
- List all houses (option 1)
- View detailed house information (option 2)
- Check pending proposals (option 3)
- Search for members (option 4)
- View system statistics (option 5)

## 🏛️ Database Architecture

### Core Tables

#### Houses
```sql
CREATE TABLE houses (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    description TEXT,
    motto TEXT,
    rules TEXT,
    founder_id INTEGER,
    net_worth REAL DEFAULT 0,
    total_members INTEGER DEFAULT 0
);
```

#### Users & Members
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT NOT NULL UNIQUE,
    email TEXT UNIQUE,
    full_name TEXT,
    password_hash TEXT NOT NULL
);

CREATE TABLE house_members (
    id INTEGER PRIMARY KEY,
    house_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    role TEXT CHECK (role IN ('founder', 'president', 'member', 'culprit')),
    contribution_score REAL DEFAULT 0,
    equity_stake REAL DEFAULT 0,
    warning_count INTEGER DEFAULT 0
);
```

#### Financial System
```sql
CREATE TABLE transactions (
    id INTEGER PRIMARY KEY,
    description TEXT NOT NULL,
    amount REAL NOT NULL,
    status TEXT DEFAULT 'pending',
    created_by INTEGER NOT NULL,
    house_id INTEGER NOT NULL
);

CREATE TABLE transaction_entries (
    id INTEGER PRIMARY KEY,
    transaction_id INTEGER NOT NULL,
    account_id INTEGER NOT NULL,
    amount REAL NOT NULL,
    entry_type TEXT CHECK (entry_type IN ('debit', 'credit'))
);
```

#### Governance System
```sql
CREATE TABLE veto_proposals (
    id INTEGER PRIMARY KEY,
    house_id INTEGER NOT NULL,
    target_member_id INTEGER NOT NULL,
    reason TEXT NOT NULL,
    votes_required INTEGER NOT NULL,
    founder_approval_required BOOLEAN DEFAULT 1
);

CREATE TABLE merge_proposals (
    id INTEGER PRIMARY KEY,
    source_house_id INTEGER NOT NULL,
    target_house_id INTEGER NOT NULL,
    terms TEXT,
    status TEXT DEFAULT 'pending'
);
```

### Advanced Tables

- **Assets** - Track property, investments, businesses
- **Accounts** - Double-entry accounting system
- **Audit Log** - Complete transaction history
- **Metrics** - Performance tracking for houses and members
- **Relationships** - Inter-house diplomatic tracking
- **Businesses** - Family business entities
- **Investments** - Portfolio management

## 🔧 Key Functions

### Database Operations
```python
from gcd_database import (
    get_db, init_db, seed_gcd_data,
    get_house_net_worth, get_member_contribution_score,
    get_pending_veto_proposals, get_house_members_by_role,
    calculate_net_time_value
)
```

### Financial Calculations
```python
# Calculate house net worth
net_worth = get_house_net_worth(house_id)

# Calculate sustainability in days
days = calculate_net_time_value(house_id, daily_expense_estimate=200)

# Get member contribution
score = get_member_contribution_score(user_id, house_id)
```

### Governance Functions
```python
# Get pending veto proposals
proposals = get_pending_veto_proposals(house_id)

# Get house members by role
members = get_house_members_by_role(house_id)
```

## 📊 Example Data Structure

### Anderson Dynasty House
- **Founder**: John Anderson (contribution: 100.0)
- **President**: Mary Anderson (contribution: 85.0)
- **Members**: Robert (75.0), Susan (70.0), James (-20.0 with 2 warnings)
- **Assets**: Family home, rental property, consulting business, investment portfolio
- **Net Worth**: ~$2.7M
- **Governance**: Active veto proposal against James

### Sample Transactions
- Monthly salary entries
- Business income from Anderson Consulting
- Mortgage payments
- Investment returns
- All with double-entry accounting

## 🎯 Core Features Implemented

### ✅ Complete House Management
- House creation and configuration
- Member roles and permissions
- Contribution scoring system
- Warning and veto tracking

### ✅ Financial System
- Double-entry accounting
- Asset valuation and tracking
- Transaction approval workflow
- Net worth calculations

### ✅ Governance System
- 9-condition veto process
- Founder approval requirements
- Weighted voting based on contribution
- House merger proposals

### ✅ Audit and Transparency
- Complete audit logging
- Transaction history tracking
- Member activity monitoring
- Performance metrics

### ✅ Advanced Features
- Net time value calculations
- Inter-house relationships
- Business entity management
- Investment portfolio tracking

## 🔒 Security Features

- **Password Hashing**: Using Werkzeug security functions
- **Role-Based Access**: Different permissions for different roles
- **Audit Logging**: Complete trail of all actions
- **Data Integrity**: Foreign key constraints and checks
- **Input Validation**: Database-level constraints

## 📈 Performance Optimizations

- **Indexes**: Strategic indexes on frequently queried columns
- **Triggers**: Automatic updates for derived values
- **Views**: Optimized queries for common operations
- **Connection Pooling**: Efficient database connections

## 🔄 Integration with Flask

The database is designed to integrate seamlessly with your Flask application:

```python
from flask import Flask
from gcd_database import init_app

app = Flask(__name__)
app.config['DATABASE'] = 'path/to/gcd_database.db'
init_app(app)
```

## 🧪 Testing the System

### CLI Commands
```bash
# Initialize database
python gcd_cli.py
# Choose option 6

# Seed example data
# Choose option 7

# View system statistics
# Choose option 5

# Explore house details
# Choose option 2, then enter house ID (usually 1)
```

### Database Queries
```sql
-- View all houses
SELECT * FROM houses;

-- View house members
SELECT hm.*, u.username, u.full_name 
FROM house_members hm 
JOIN users u ON hm.user_id = u.id 
WHERE hm.house_id = 1;

-- View recent transactions
SELECT t.*, u.username as created_by_name 
FROM transactions t 
JOIN users u ON t.created_by = u.id 
WHERE t.house_id = 1 
ORDER BY t.created_at DESC 
LIMIT 10;
```

## 🚀 Next Steps

### For Development
1. **Flask Integration**: Connect to your existing Flask app
2. **API Development**: Create REST endpoints for all operations
3. **Frontend Integration**: Build web interface for house management
4. **Blockchain Integration**: Add actual blockchain transaction recording

### For Production
1. **Security Audit**: Review all security measures
2. **Performance Testing**: Load testing with large datasets
3. **Backup Strategy**: Implement regular database backups
4. **Monitoring**: Add system health monitoring

## 📚 Documentation

- **Schema Documentation**: See comments in `gcd_schema.sql`
- **Function Documentation**: See docstrings in `gcd_database.py`
- **CLI Help**: Run `python gcd_cli.py` and explore the menu

## 🤝 Contributing

To extend the GCD database:

1. **Add New Tables**: Update `gcd_schema.sql`
2. **Add Functions**: Implement in `gcd_database.py`
3. **Update CLI**: Add menu options in `gcd_cli.py`
4. **Update Tests**: Add test cases for new functionality

## 📞 Support

For questions about the GCD database system:

1. Check the CLI help system
2. Review the schema and function documentation
3. Examine the example data for usage patterns
4. Test with the CLI interface before integration

---

**This database system implements the complete vision of Generis Citadel Dynasty - a revolutionary approach to family financial management and generational wealth preservation.**
