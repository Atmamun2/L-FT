# PythonAnywhere Exact Step-by-Step Instructions

## 🎯 Pre-Deployment Checklist (Local)

Before starting, ensure your local app runs without errors:
```bash
cd /Users/atmamun/Programming/SOFT12/L-FT/ledger_of_financial_transactions
python run.py
```

## 📋 Step 1: PythonAnywhere Account Setup

1. **Sign Up**: Go to https://www.pythonanywhere.com/
2. **Create Account**: Choose "Beginner" (Free) or "Custom" (Paid)
3. **Verify Email**: Check your email and verify your account

## 📁 Step 2: Upload Your Code

### Option A: Using Git (Recommended)
1. **Push to GitHub**:
```bash
git init
git add .
git commit -m "Initial commit for PythonAnywhere deployment"
git branch -M main
git remote add origin https://github.com/yourusername/financial-ledger.git
git push -u origin main
```

2. **Clone on PythonAnywhere**:
- Go to PythonAnywhere "Bash" console
- Run: `git clone https://github.com/yourusername/financial-ledger.git`
- Run: `cd financial-ledger`

### Option B: Manual Upload
1. **Create ZIP**: Zip your entire project folder
2. **Upload**: Go to "Files" tab → "Upload a file"
3. **Extract**: Right-click ZIP → "Unzip archive"

## 🗄️ Step 3: Set Up Database

1. **Go to "Databases" tab**
2. **Create MySQL Database**:
   - Database name: `yourusername$financial_ledger`
   - Password: Generate a strong password
   - Note: Save these credentials!

3. **Update Environment Variables**:
```bash
cd /home/yourusername/financial-ledger
cp .env.pythonanywhere .env
nano .env
```

4. **Edit `.env` file** (replace with your actual values):
```env
FLASK_CONFIG=pythonanywhere
FLASK_ENV=production
FLASK_DEBUG=0
SECRET_KEY=generate-a-32-character-random-string-here
DATABASE_URL=mysql://yourusername:yourpassword@yourusername.mysql.pythonanywhere-services.com/yourusername$financial_ledger
```

## 📦 Step 4: Install Dependencies

In PythonAnywhere Bash console:
```bash
cd /home/yourusername/financial-ledger
pip install -r requirements.txt
```

**Verify installation**:
```bash
pip list | grep Flask
```

## 🌐 Step 5: Create Web App

1. **Go to "Web" tab**
2. **Click "Add a new web app"**
3. **Select Framework**: Flask
4. **Python Version**: Python 3.11 (or latest)
5. **Project Path**: `/home/yourusername/financial-ledger`
6. **Click Next**

## ⚙️ Step 6: Configure WSGI

1. **Go to "Web" tab → "WSGI configuration file"**
2. **Click the link to edit the file**
3. **Replace entire content** with:

```python
#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
from pathlib import Path

# Add the project directory to the Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Set environment variables for production
os.environ['FLASK_CONFIG'] = 'pythonanywhere'
os.environ['FLASK_ENV'] = 'production'
os.environ['FLASK_DEBUG'] = '0'

# Import the application
from wsgi import application as app

# This is what PythonAnywhere will look for
application = app
```

4. **Save** the file (Ctrl+O, then Ctrl+X in nano)

## 🗃️ Step 7: Initialize Database

1. **In Bash console**:
```bash
cd /home/yourusername/financial-ledger
python deploy_pythonanywhere.py
```

2. **Expected output**:
```
Creating database tables...
Admin user created. Please change the default password!
Deployment completed successfully!
```

## 🔄 Step 8: Test and Reload

1. **Check for errors**:
```bash
python -c "from pythonanywhere_wsgi import application; print('WSGI file loads successfully')"
```

2. **Reload Web App**:
- Go to "Web" tab
- Click the big green **"Reload"** button

3. **Check Status**:
- Look for "Site is running" message
- Click your URL to test

## 🐛 Step 9: Troubleshooting

### If you get a 500 error:

1. **Check error logs**:
- Go to "Web" tab
- Look at "Error log" section
- Note any error messages

2. **Common fixes**:
```bash
# Check Python path
python -c "import sys; print(sys.path)"

# Test imports
python -c "from app import create_app; print('App imports successfully')"

# Check database connection
python -c "from app import create_app, db; app = create_app('pythonanywhere'); app.app_context().push(); print('Database connected')"
```

### If static files don't load:
```bash
# Check static directory
ls -la /home/yourusername/financial-ledger/app/static/
```

## 🔐 Step 10: Security Setup

1. **Change admin password**:
- Visit your site
- Log in with: username `admin`, password `admin123`
- Go to profile and change password immediately

2. **Generate real SECRET_KEY**:
```python
import secrets
print(secrets.token_hex(32))
```
- Update `.env` with this key

## ✅ Step 11: Final Verification

1. **Test all features**:
- User registration
- Login/logout
- Add transaction
- View dashboard
- Edit/delete transaction

2. **Check logs regularly**:
```bash
tail -f /var/log/yourusername.error.log
```

## 📱 Step 12: Share Your App

Your app is live at: `https://yourusername.pythonanywhere.com/`

## 🆘 Emergency Commands

If something goes wrong:
```bash
# Restart web app
touch /var/www/yourusername_pythonanywhere_com_wsgi.py

# Check processes
ps aux | grep python

# Kill stuck processes
pkill -f python
```

## 📞 Getting Help

- **PythonAnywhere Forums**: https://www.pythonanywhere.com/forums/
- **Error Logs**: Your best debugging tool
- **PythonAnywhere Docs**: https://help.pythonanywhere.com/

## 🎉 Success!

Your Financial Ledger is now live on PythonAnywhere! Users can register, log in, and manage their financial transactions from anywhere in the world.

Remember to monitor your app and keep dependencies updated!
