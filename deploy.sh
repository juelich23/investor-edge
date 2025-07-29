#!/bin/bash

echo "🚀 Investor Edge Platform - Quick Deploy Script"
echo "============================================="

# Check if git is initialized
if [ ! -d .git ]; then
    echo "📁 Initializing git repository..."
    git init
    git branch -M main
fi

# Add all files
echo "📦 Adding files to git..."
git add .

# Commit
echo "💾 Creating commit..."
git commit -m "Deploy: Investor Edge Platform $(date +%Y-%m-%d)"

# Check if remote exists
if ! git remote | grep -q origin; then
    echo ""
    echo "⚠️  No git remote found!"
    echo "Please add your GitHub repository:"
    echo ""
    echo "1. Create a new repo on GitHub (suggested name: investor-edge)"
    echo "2. Run: git remote add origin https://github.com/YOUR_USERNAME/investor-edge.git"
    echo "3. Run this script again"
    exit 1
fi

# Push to GitHub
echo "🔄 Pushing to GitHub..."
git push -u origin main

echo ""
echo "✅ Code pushed to GitHub!"
echo ""
echo "📋 Next Steps:"
echo "============="
echo ""
echo "1. BACKEND DEPLOYMENT (Render):"
echo "   - Go to https://render.com"
echo "   - Click 'New +' → 'Web Service'"
echo "   - Connect your GitHub repo"
echo "   - Use these settings:"
echo "     • Build Command: pip install -r requirements.txt"
echo "     • Start Command: cd backend && uvicorn main:app --host 0.0.0.0 --port \$PORT"
echo "   - Add environment variable:"
echo "     • ANTHROPIC_API_KEY = [Your API Key]"
echo ""
echo "2. FRONTEND DEPLOYMENT (Vercel):"
echo "   - Go to https://vercel.com"
echo "   - Import your GitHub repo"
echo "   - Set root directory to: frontend"
echo "   - Add environment variable:"
echo "     • REACT_APP_API_URL = [Your Render URL]"
echo ""
echo "3. UPDATE BACKEND:"
echo "   - Add FRONTEND_URL = [Your Vercel URL] to Render env vars"
echo ""
echo "📱 Share with friends: https://[your-app].vercel.app"