#!/bin/bash

echo "🚀 Setting up Investor Edge Platform..."

# Backend setup
echo "📦 Setting up backend..."
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Check for .env file
if [ ! -f .env ]; then
    echo "⚠️  Creating .env file from template..."
    cp .env.example .env
    echo "📝 Please add your API keys to backend/.env"
fi

# Initialize database
echo "🗄️  Initializing database..."
python database.py

# Process initial data
echo "🔄 Processing earnings data..."
python process_all.py

cd ..

# Frontend setup
echo "📦 Setting up frontend..."
cd frontend
npm install

echo "✅ Setup complete!"
echo ""
echo "To start the application:"
echo "1. Backend: cd backend && source venv/bin/activate && uvicorn main:app --reload"
echo "2. Frontend: cd frontend && npm start"
echo ""
echo "Don't forget to add your API keys to backend/.env!"