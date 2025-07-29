# Deployment Guide for Investor Edge Platform (Render + Vercel)

## Quick Start - Render Backend Deployment

Render handles monorepos better than Railway. Here's how to deploy:

### Step 1: Push to GitHub

```bash
# In your project root
cd /Users/nickjuelich/Desktop/Code/investor
git init
git add .
git commit -m "Initial commit - Investor Edge Platform"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/investor-edge.git
git push -u origin main
```

### Step 2: Deploy Backend to Render

1. Go to [Render.com](https://render.com)
2. Click "New +" → "Web Service"
3. Connect your GitHub account and select your repository
4. Configure the service:
   - **Name**: investor-edge-api
   - **Root Directory**: Leave blank (monorepo root)
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT`
5. Add environment variables:
   - `ANTHROPIC_API_KEY`: Your API key
   - `ENVIRONMENT`: production
   - `FRONTEND_URL`: https://investor-edge.vercel.app (update after frontend deploy)
6. Click "Create Web Service"
7. Wait for deployment (takes 5-10 minutes)
8. You'll get a URL like: `https://investor-edge-api.onrender.com`

### Step 3: Deploy Frontend to Vercel

1. Go to [Vercel.com](https://vercel.com)
2. Click "Add New..." → "Project"
3. Import your GitHub repository
4. Configure:
   - **Framework Preset**: Create React App
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `build`
5. Add environment variable:
   - `REACT_APP_API_URL`: Your Render backend URL (e.g., https://investor-edge-api.onrender.com)
6. Click "Deploy"
7. You'll get a URL like: `https://investor-edge.vercel.app`

### Step 4: Update Backend CORS

1. Go back to Render dashboard
2. Go to Environment → Edit `FRONTEND_URL`
3. Set it to your Vercel URL
4. Save and let it redeploy

## Alternative: One-Click Deploy with Render

If the above doesn't work, use the render.yaml file I created:

1. In Render dashboard, click "New +" → "Blueprint"
2. Connect your GitHub repo
3. Render will detect the `render.yaml` and set everything up
4. Just add your `ANTHROPIC_API_KEY` in the environment variables

## Testing Your Deployment

1. **Backend Health Check**: 
   ```
   curl https://investor-edge-api.onrender.com/
   ```
   Should return: "Investor Edge API is running"

2. **Frontend**: Visit your Vercel URL and try searching for stocks

## Troubleshooting

### If Backend Won't Deploy:
1. Check Render logs for errors
2. Make sure Python version matches (3.11.6)
3. Try manual deploy:
   ```bash
   # SSH into Render console
   cd backend
   pip install -r requirements.txt
   uvicorn main:app --host 0.0.0.0 --port $PORT
   ```

### If Frontend Can't Connect:
1. Check browser console for CORS errors
2. Verify `REACT_APP_API_URL` is set correctly
3. Make sure backend URL doesn't have trailing slash

## Future Updates

After initial deployment, all pushes to GitHub main branch will auto-deploy:

```bash
# Make changes
git add .
git commit -m "Update: Added new feature"
git push origin main
# Both services auto-deploy!
```

## Costs
- **Render**: Free tier includes 750 hours/month
- **Vercel**: Free tier includes 100GB bandwidth/month
- **Total**: $0 for personal use

## Share with Friends

Once deployed, share: `https://investor-edge.vercel.app`

Your friends can now:
- Search any NYSE/NASDAQ stock
- View AI-powered earnings summaries
- See historical trends
- Analyze earnings call transcripts