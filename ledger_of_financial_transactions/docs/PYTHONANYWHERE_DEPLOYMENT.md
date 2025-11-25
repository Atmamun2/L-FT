# PythonAnywhere Deployment Guide

This guide will help you deploy your Flask Financial Ledger application to PythonAnywhere.

## 🚀 Quick Start

### 1. Set Up PythonAnywhere Account
1. Sign up for a [PythonAnywhere](https://www.pythonanywhere.com/) account
2. Choose a plan (Free tier works for basic testing)

### 2. Create a Web App
1. Go to "Web" tab in PythonAnywhere dashboard
2. Click "Add a new web app"
3. Choose "Flask" framework
4. Python version: 3.11 (or latest available)
5. Project name: `financial-ledger`

### 3. Upload Your Code
1. Go to "Files" tab
2. Upload your entire project folder
3. Or use Git: `git clone your-repo-url` in Bash console

### 4. Configure Database
1. Go to "Databases" tab
2. Create a MySQL database
3. Note your database credentials
4. Update `.env.pythonanywhere` with your database URL

### 5. Install Dependencies
In the PythonAnywhere Bash console:
```bash
cd /path/to/your/project
pip install -r requirements.txt
```

### 6. Configure Environment Variables
1. Copy `.env.pythonanywhere` to `.env`
2. Edit the file with your actual values:
```bash
cp .env.pythonanywhere .env
nano .env
```

### 7. Set Up WSGI
1. Go to "Web" tab → "WSGI configuration file"
2. Replace the contents with your `pythonanywhere_wsgi.py` content
3. Or upload your `pythonanywhere_wsgi.py` and reference it

### 8. Initialize Database
Run the deployment script:
```bash
python deploy_pythonanywhere.py
```

### 9. Reload Web App
1. Go to "Web" tab
2. Click "Reload" button
3. Your app should be live!

## 🔧 Detailed Configuration

### Environment Variables
Create `.env` file in your project root:
```env
FLASK_CONFIG=pythonanywhere
FLASK_ENV=production
FLASK_DEBUG=0
SECRET_KEY=your-super-secret-key-here
DATABASE_URL=mysql://username:password@username.mysql.pythonanywhere-services.com/dbname
```

### WSGI Configuration
Your WSGI file should point to:
```python
from pythonanywhere_wsgi import application
```

### Static Files
Your static files are automatically served from `/static/` URL.

## 🛠️ Troubleshooting

### Common Issues

**500 Internal Server Error**
- Check the error logs in "Web" tab
- Ensure all dependencies are installed
- Verify database connection string

**Database Connection Error**
- Verify MySQL database is created
- Check database credentials in `.env`
- Ensure database user has proper permissions

**Static Files Not Loading**
- Check that static files are in `/app/static/` directory
- Verify file permissions
- Restart web app

**Import Errors**
- Ensure project structure is maintained
- Check Python path in WSGI file
- Verify all required files are uploaded

### Useful Commands
```bash
# Check installed packages
pip list

# Check Python path
python -c "import sys; print(sys.path)"

# Test database connection
python -c "from app import create_app, db; app = create_app('pythonanywhere'); app.app_context().push(); print('Database connected')"

# Check logs
tail -n 50 /var/log/your-user-name.error.log
```

## 📁 Required Files Structure
```
/home/yourusername/financial-ledger/
├── app/
│   ├── __init__.py
│   ├── models/
│   ├── routes/
│   ├── forms/
│   ├── templates/
│   └── static/
├── migrations/
├── pythonanywhere_wsgi.py
├── deploy_pythonanywhere.py
├── requirements.txt
├── config.py
├── run.py
├── wsgi.py
└── .env
```

## 🔒 Security Notes

1. **Change Default Passwords**: Update the admin password after first login
2. **Secret Key**: Use a strong, random SECRET_KEY
3. **Database Security**: Use strong database passwords
4. **HTTPS**: PythonAnywhere provides HTTPS automatically
5. **Environment Variables**: Never commit `.env` files to version control

## 📈 Performance Tips

1. **Database Optimization**: Use MySQL instead of SQLite for production
2. **Static Files**: Consider CDN for static assets
3. **Caching**: Enable Flask-Caching if needed
4. **Logging**: Monitor error logs regularly

## 🆘 Getting Help

- PythonAnywhere documentation: https://help.pythonanywhere.com/
- Flask deployment guide: https://flask.palletsprojects.com/en/latest/tutorial/deploy/
- Error logs are your best friend - check them first!

## 🎉 Success!

Your Financial Ledger application is now live on PythonAnywhere! Users can:
- Register new accounts
- Log in and manage transactions
- View financial dashboard
- Add, edit, and delete transactions

Remember to monitor your application and keep dependencies updated!
