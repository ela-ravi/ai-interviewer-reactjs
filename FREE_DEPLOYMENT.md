# Free Deployment Guide

## 🎯 Best Free Options

### Option 1: Render.com (Recommended) ⭐

**Perfect for:** Full-stack apps with Docker

#### Setup Steps:

1. **Prepare Your Code**
```bash
# Push to GitHub
git init
git add .
git commit -m "Deploy to Render"
git push origin main
```

2. **Deploy Backend**
- Go to https://render.com/
- Click "New +" → "Web Service"
- Connect your GitHub repo
- Settings:
  - Name: `ai-interviewer-backend`
  - Root Directory: `backend`
  - Environment: `Docker`
  - Instance Type: `Free`
- Add Environment Variable:
  - `OPENROUTER_API_KEY`: your_key_here
  - `CORS_ORIGINS`: `*`
- Click "Create Web Service"

3. **Deploy Frontend**
- Click "New +" → "Static Site"
- Connect same GitHub repo
- Settings:
  - Name: `ai-interviewer-frontend`
  - Root Directory: `frontend`
  - Build Command: `npm install && npm run build`
  - Publish Directory: `dist`
- Add Environment Variable:
  - `VITE_API_URL`: https://ai-interviewer-backend.onrender.com/api
- Click "Create Static Site"

**Your app is live!** 🎉
- Frontend: https://ai-interviewer-frontend.onrender.com
- Backend: https://ai-interviewer-backend.onrender.com

**⚠️ Note:** Free tier apps sleep after 15 min of inactivity. First request takes ~1 min to wake up.

---

### Option 2: Railway.app ⭐

**Perfect for:** No cold starts, great UX

#### Setup Steps:

1. **Install Railway CLI**
```bash
npm install -g @railway/cli
```

2. **Deploy**
```bash
railway login
railway init
railway up
```

3. **Add Environment Variables**
```bash
railway variables set OPENROUTER_API_KEY=your_key_here
railway variables set CORS_ORIGINS="*"
```

**Cost:** $5/month credit (free tier)

---

### Option 3: Vercel (Frontend) + Render (Backend)

**Perfect for:** Best performance, unlimited bandwidth

#### Frontend on Vercel:

```bash
cd frontend
npm install -g vercel
vercel
```

Follow prompts:
- Project name: `ai-interviewer`
- Build command: `npm run build`
- Output directory: `dist`

#### Backend on Render:
(Same as Option 1 backend steps)

#### Update Frontend:
```bash
# Set backend URL
vercel env add VITE_API_URL production
# Enter: https://your-backend.onrender.com/api
```

---

### Option 4: Fly.io

**Perfect for:** Global deployment, Docker Compose

```bash
# Install flyctl
curl -L https://fly.io/install.sh | sh

# Login
flyctl auth login

# Launch backend
cd backend
flyctl launch --name ai-interviewer-backend
flyctl secrets set OPENROUTER_API_KEY=your_key_here

# Deploy
flyctl deploy
```

---

### Option 5: Replit (Easiest)

**Perfect for:** Quick demos, no setup

1. Go to https://replit.com
2. Click "Create Repl"
3. Select "Import from GitHub"
4. Paste your repo URL
5. Click "Import"
6. Add secrets (🔒 icon):
   - `OPENROUTER_API_KEY`
7. Click "Run"

**Your app is live!** Gets a free replit.app subdomain

---

## 📊 Comparison

| Platform | Setup | Cold Start | Bandwidth | Best For |
|----------|-------|------------|-----------|----------|
| **Render** ⭐ | Easy | Yes (~1min) | Limited | Full-stack Docker apps |
| **Railway** ⭐ | Easy | No | Limited | Fast apps, no sleep |
| **Vercel** ⭐⭐ | Easy | No | Unlimited | Frontend only |
| **Fly.io** | Medium | No | 160GB | Global deployment |
| **Replit** | Easiest | No | Limited | Quick demos |

---

## 💡 Tips for Free Tier

1. **Keep App Awake:**
   - Use UptimeRobot.com to ping your app every 5 minutes
   - Prevents sleep on Render

2. **Optimize Costs:**
   - Use Vercel for frontend (unlimited bandwidth)
   - Use Railway/Render for backend only

3. **Database:**
   - Use Supabase (free PostgreSQL)
   - Or MongoDB Atlas (free 512MB)

4. **Domain:**
   - Get free subdomain from platform
   - Or use Freenom for custom domain

---

## 🚀 Quick Deploy Commands

### Render (via render.yaml)
```bash
# Just push to GitHub, Render auto-deploys from render.yaml
git push origin main
```

### Railway
```bash
railway login
railway up
railway open
```

### Vercel (Frontend)
```bash
cd frontend
vercel --prod
```

### Fly.io
```bash
flyctl deploy
flyctl open
```

---

## ⚠️ Important Notes

1. **API Key Security:**
   - Never commit `.env` files
   - Use platform's secrets/environment variables

2. **CORS:**
   - Update `CORS_ORIGINS` in production
   - Use your actual frontend URL

3. **Session Storage:**
   - Current implementation uses memory (lost on restart)
   - For production, add Redis (most platforms offer free tier)

4. **Costs:**
   - Monitor usage to stay within free tier
   - Railway: Watch $5/month credit
   - Render: Watch 750 hour/month limit

---

## 🆘 Troubleshooting

### App Won't Start
- Check logs: `railway logs` or Render dashboard
- Verify environment variables are set
- Check Docker build succeeded

### CORS Errors
- Set `CORS_ORIGINS=*` for testing
- Update to specific domain in production

### 502/504 Errors
- App is sleeping (wait 1 minute)
- Or check health endpoint: `/health`

---

## 📚 Resources

- Render Docs: https://render.com/docs
- Railway Docs: https://docs.railway.app
- Vercel Docs: https://vercel.com/docs
- Fly.io Docs: https://fly.io/docs

---

**Choose based on your needs:**
- **Easiest:** Replit
- **Best Free:** Render or Railway
- **Best Performance:** Vercel (frontend) + Railway (backend)
- **Most Flexible:** Fly.io

