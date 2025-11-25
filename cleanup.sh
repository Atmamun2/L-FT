#!/bin/bash

# Make the script executable
chmod +x "$0"

echo "🚀 Starting cleanup process..."

# Remove system files
echo "🧹 Removing system files..."
find . -name ".DS_Store" -delete
find . -name "__MACOSX" -exec rm -rf {} + 2>/dev/null

# Remove old wireframe files
echo "🗑️ Removing old wireframe files..."
rm -f "gcd-wireframe.jsx"
rm -f "loft-wireframe.html"
rm -f "loft-wireframe.jsx"
rm -f "network-state-wireframe.jsx"

# Remove Python cache files
echo "🗑️ Removing Python cache files..."
find . -type d -name "__pycache__" -exec rm -rf {} +
find . -type f -name "*.py[co]" -delete
find . -type d -name "*.egg-info" -exec rm -rf {} +

# Clean up database files (keeping the main database)
echo "💾 Cleaning up database files..."
# Keep only the main database file used by the application
if [ -f "backend/instance/site.db" ]; then
    echo "🔍 Found main database file: backend/instance/site.db"
    # Create backup of the main database
    cp "backend/instance/site.db" "backend/instance/site.db.backup"
    echo "✅ Created backup of main database at: backend/instance/site.db.backup"
    
    # Remove other database files
    rm -f "backend/financial_transactions.db"
    rm -f "backend/gcd_schema.sql"
    rm -f "backend/gcd_schematic.sql"
    rm -f "backend/schema.sql"
    rm -f "backend/init_database.sql"
    echo "✅ Removed redundant database files"
else
    echo "⚠️  Main database file not found at backend/instance/site.db"
    echo "⚠️  Please verify the correct database file location before removing others"
fi

# Remove virtual environment (can be recreated with requirements.txt)
echo "🧹 Removing virtual environment..."
rm -rf "venv"

# Clean up logs
echo "📝 Cleaning up logs..."
rm -rf "backend/logs"

# Clean up frontend build files
echo "🧹 Cleaning up frontend build files..."
rm -rf "loft-financial-dashboard/node_modules"
rm -rf "loft-financial-dashboard/dist"
rm -rf "loft-financial-dashboard/.vite"

# Remove any remaining cache directories
echo "🧹 Removing cache directories..."
find . -type d -name ".pytest_cache" -exec rm -rf {} +
find . -type d -name ".mypy_cache" -exec rm -rf {} +

# Remove any .pyc files
find . -name "*.pyc" -delete

# Remove empty directories
echo "🧹 Removing empty directories..."
find . -type d -empty -delete

echo "✨ Cleanup complete!"
echo "✅ Project has been cleaned up successfully"
echo "📋 Next steps:"
echo "1. Review the changes with: git status"
echo "2. If everything looks good, commit the changes"
echo "3. Recreate virtual environment if needed:"
echo "   cd backend && python -m venv venv && source venv/bin/activate && pip install -r requirements.txt"
echo "4. Reinstall frontend dependencies if needed:"
echo "   cd loft-financial-dashboard && npm install"
