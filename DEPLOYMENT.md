# Deployment Guide for Investor Edge Platform

## Overview
- **Frontend**: Deployed on Vercel (React app)
- **Backend**: Deployed on Railway or Render (FastAPI)
- **Data Storage**: JSON files in the backend (can upgrade to PostgreSQL later)

## Prerequisites
1. GitHub account
2. Vercel account (free)
3. Railway or Render account (free tier available)
4. Your Anthropic API key

## Step 1: Push to GitHub

First, create a new GitHub repository:
```bash
# Initialize git in the project root
cd /Users/nickjuelich/Desktop/Code/investor
git init

# Create main branch
git checkout -b main

# Add all files
git add .

# Commit
git commit -m "Initial commit - Investor Edge Platform"

# Add your GitHub remote
git remote add origin https://github.com/YOUR_USERNAME/investor-edge.git

# Push to GitHub
git push -u origin main
```

## Step 2: Deploy Backend to Railway

1. Go to [Railway.app](https://railway.app)
2. Click "New Project" → "Deploy from GitHub repo"
3. Select your `investor-edge` repository
4. Railway will auto-detect it's a Python app
5. Add environment variables:
   - `ANTHROPIC_API_KEY`: Your API key
   - `ENVIRONMENT`: production
   - `FRONTEND_URL`: https://your-app.vercel.app (you'll get this after deploying frontend)
6. Railway will provide you with a URL like: `https://investor-edge-backend.up.railway.app`

## Step 3: Deploy Frontend to Vercel

1. Go to [Vercel.com](https://vercel.com)
2. Click "New Project" → Import your GitHub repo
3. Select the `frontend` directory as the root
4. Add environment variable:
   - `REACT_APP_API_URL`: Your Railway backend URL (e.g., https://investor-edge-backend.up.railway.app)
5. Deploy!
6. You'll get a URL like: `https://investor-edge.vercel.app`

## Step 4: Update Backend CORS

1. Go back to Railway
2. Update the `FRONTEND_URL` environment variable with your Vercel URL
3. Redeploy the backend

## Step 5: Create Data Directories

SSH into your Railway app or use the Railway CLI:
```bash
mkdir -p data/summaries data/transcripts data/historical data/analyses
```

## Continuous Deployment

Both Vercel and Railway support automatic deployments:

### For Frontend Updates:
```bash
cd frontend
# Make your changes
git add .
git commit -m "Update: [description]"
git push origin main
# Vercel automatically deploys!
```

### For Backend Updates:
```bash
cd backend
# Make your changes
git add .
git commit -m "Update: [description]"
git push origin main
# Railway automatically deploys!
```

## Environment Variables Summary

### Backend (Railway):
- `ANTHROPIC_API_KEY`: Your Anthropic API key
- `ENVIRONMENT`: production
- `FRONTEND_URL`: https://your-app.vercel.app
- `PORT`: (Railway sets this automatically)

### Frontend (Vercel):
- `REACT_APP_API_URL`: https://your-backend.up.railway.app

## Monitoring

- **Frontend logs**: Vercel dashboard → Functions tab
- **Backend logs**: Railway dashboard → Deployments → View logs
- **API health check**: Visit `https://your-backend.up.railway.app/` (should return "Investor Edge API is running")

## Sharing with Friends

Once deployed, share your Vercel URL (e.g., `https://investor-edge.vercel.app`) with friends!

## Cost Estimates

- **Vercel**: Free tier includes 100GB bandwidth/month
- **Railway**: Free tier includes $5 credit/month (enough for ~500 hours)
- **Total**: ~$0-5/month for light usage

## Upgrading Later

When ready to scale:
1. Add PostgreSQL database (Railway provides this)
2. Implement caching with Redis
3. Add authentication with Auth0 or Clerk
4. Set up custom domain