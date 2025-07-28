#!/bin/bash

echo "🚀 Setting up Investor Edge for production deployment"

# Check if .env exists in backend
if [ ! -f backend/.env ]; then
    echo "❌ backend/.env file not found!"
    echo "Please create backend/.env with:"
    echo "ANTHROPIC_API_KEY=your_key_here"
    exit 1
fi

# Build frontend
echo "📦 Building frontend..."
cd frontend
npm run build

# Create necessary data directories
echo "📁 Creating data directories..."
cd ../backend
mkdir -p ../data/summaries ../data/transcripts ../data/historical ../data/analyses ../data/transcripts/full

echo "✅ Production setup complete!"
echo ""
echo "Next steps:"
echo "1. Push to GitHub: git push origin main"
echo "2. Deploy backend to Railway"
echo "3. Deploy frontend to Vercel"
echo "4. Update environment variables"
echo ""
echo "See DEPLOYMENT.md for detailed instructions"