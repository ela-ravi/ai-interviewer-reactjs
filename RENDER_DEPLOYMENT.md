# Render.com Deployment Guide

## 🚀 Quick Deploy to Render.com

### Step 1: Deploy Backend

1. Go to https://render.com/dashboard
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub repository
4. Configure:
   - **Name**: `ai-interviewer-backend`
   - **Region**: Choose closest to you
   - **Branch**: `main`
   - **Root Directory**: `backend`
   - **Runtime**: `Docker`
   - **Instance Type**: `Free`

5. **Environment Variables** (Click "Advanced" → "Add Environment Variable"):
   ```
   OPENROUTER_API_KEY=your_actual_key_here
   FLASK_ENV=production
   FLASK_DEBUG=False
   SECRET_KEY=<generate-random-string>
   CORS_ORIGINS=https://ai-interviewer-reactjs.onrender.com
   MODEL=mistralai/mistral-small-creative
   TEMPERATURE=0.7
   ```

6. Click **"Create Web Service"**
7. Wait for deployment (takes ~5-10 minutes)
8. **Copy your backend URL**: e.g., `https://ai-interviewer-backend.onrender.com`

### Step 2: Deploy Frontend

1. Click **"New +"** → **"Static Site"**
2. Connect same GitHub repository
3. Configure:
   - **Name**: `ai-interviewer-reactjs`
   - **Branch**: `main`
   - **Root Directory**: `frontend`
   - **Build Command**: `npm install && npm run build`
   - **Publish Directory**: `dist`

4. **Environment Variables**:
   ```
   VITE_API_URL=https://ai-interviewer-backend.onrender.com/api
   ```

5. Click **"Create Static Site"**
6. Wait for deployment (takes ~3-5 minutes)

### Step 3: Update Backend CORS

**IMPORTANT**: After frontend is deployed, update backend CORS:

1. Go to your **backend service** in Render dashboard
2. Click **"Environment"** tab
3. Update `CORS_ORIGINS` to:
   ```
   CORS_ORIGINS=https://ai-interviewer-reactjs.onrender.com,https://ai-interviewer-reactjs.onrender.com/
   ```
   
   Note: Include both with and without trailing slash

4. Click **"Save Changes"**
5. Backend will auto-redeploy

## ✅ Verify Deployment

### Test Backend:
```bash
# Health check
curl https://ai-interviewer-backend.onrender.com/health

# Should return:
# {"status":"healthy","service":"ai-interviewer-backend"}
```

### Test Frontend:
Open browser: https://ai-interviewer-reactjs.onrender.com

### Test CORS:
```bash
curl -H "Origin: https://ai-interviewer-reactjs.onrender.com" \
     -H "Access-Control-Request-Method: POST" \
     -H "Access-Control-Request-Headers: Content-Type" \
     -X OPTIONS \
     https://ai-interviewer-backend.onrender.com/api/interview/create \
     -v
```

Should see: `Access-Control-Allow-Origin: https://ai-interviewer-reactjs.onrender.com`

## 🔧 Common Issues & Fixes

### Issue 1: CORS Error ❌

**Error**: "Access to fetch has been blocked by CORS policy"

**Fix**:
1. Check backend `CORS_ORIGINS` includes exact frontend URL
2. Include both with/without trailing slash:
   ```
   CORS_ORIGINS=https://ai-interviewer-reactjs.onrender.com,https://ai-interviewer-reactjs.onrender.com/
   ```
3. Redeploy backend

### Issue 2: Backend Returns 502 ❌

**Cause**: Free tier apps sleep after 15 minutes of inactivity

**Fix**: 
1. Wait ~1 minute for app to wake up
2. Use UptimeRobot to keep it awake:
   - Go to https://uptimerobot.com (free)
   - Add monitor: your backend URL + `/health`
   - Check every 5 minutes

### Issue 3: Environment Variables Not Working ❌

**Fix**:
1. Check spelling exactly matches
2. No quotes around values in Render UI
3. Click "Save Changes" after editing
4. Check deployment logs for errors

### Issue 4: Build Fails ❌

**Backend Build Error**:
```bash
# Check logs in Render dashboard
# Common fix: Verify Dockerfile path is correct
```

**Frontend Build Error**:
```bash
# Check VITE_API_URL is set
# Verify build command: npm install && npm run build
# Verify publish directory: dist
```

## 📊 Render Free Tier Limits

- ✅ 750 hours/month free compute
- ✅ Auto-sleep after 15 min inactivity
- ✅ Cold start: ~30-60 seconds
- ✅ 100GB bandwidth/month
- ✅ Free SSL certificates
- ⚠️ Logs retained for 7 days

## 🔒 Security Checklist

- [x] `OPENROUTER_API_KEY` set as environment variable
- [x] `SECRET_KEY` changed from default
- [x] `FLASK_DEBUG=False` in production
- [x] `CORS_ORIGINS` set to specific frontend URL
- [x] HTTPS enabled (automatic on Render)
- [x] `.env` files not committed to Git

## 🚀 Auto-Deploy Setup

Render auto-deploys on Git push:

1. Go to service settings
2. Enable **"Auto-Deploy"**
3. Now pushing to `main` branch auto-deploys

```bash
git add .
git commit -m "Update feature"
git push origin main
# Render automatically deploys! 🎉
```

## 📱 Custom Domain (Optional)

### Add Custom Domain:

1. Go to service **"Settings"**
2. Click **"Custom Domain"**
3. Add your domain: `interview.yourdomain.com`
4. Add DNS records (shown in Render):
   ```
   Type: CNAME
   Name: interview
   Value: ai-interviewer-backend.onrender.com
   ```

5. Wait for DNS propagation (~1 hour)
6. Update `CORS_ORIGINS` to include custom domain

## 🔍 Monitoring & Logs

### View Logs:
1. Go to service in Render dashboard
2. Click **"Logs"** tab
3. Real-time logs appear here

### Metrics:
1. Click **"Metrics"** tab
2. View:
   - CPU usage
   - Memory usage
   - Request count
   - Response times

## 💰 Cost Optimization

### Keep Free:
1. Use free tier (750 hours/month)
2. One backend + one frontend = FREE
3. Keep app awake with UptimeRobot

### Upgrade If Needed:
- **Starter**: $7/month (no sleep)
- **Standard**: $25/month (more resources)

## 🆘 Troubleshooting Commands

```bash
# Test backend health
curl https://your-backend.onrender.com/health

# Test with CORS headers
curl -H "Origin: https://your-frontend.onrender.com" \
     https://your-backend.onrender.com/api/interview/create -v

# Test API endpoint
curl -X POST https://your-backend.onrender.com/api/interview/create \
  -H "Content-Type: application/json" \
  -d '{"technology":"Python","position":"Developer"}'
```

## 📚 Environment Variables Template

### Backend Production:
```bash
OPENROUTER_API_KEY=sk-or-v1-xxx...
FLASK_ENV=production
FLASK_DEBUG=False
SECRET_KEY=<use: openssl rand -hex 32>
CORS_ORIGINS=https://ai-interviewer-reactjs.onrender.com
PORT=10000
MODEL=mistralai/mistral-small-creative
TEMPERATURE=0.7
SESSION_TIMEOUT_HOURS=2
```

### Frontend Production:
```bash
VITE_API_URL=https://ai-interviewer-backend.onrender.com/api
VITE_APP_NAME=AI Interviewer
VITE_ENABLE_DEBUG=false
```

## ✨ Success Checklist

- [x] Backend deployed and healthy
- [x] Frontend deployed and accessible
- [x] CORS configured correctly
- [x] API key working
- [x] Can create interview session
- [x] Can start interview
- [x] Can submit answers
- [x] Feedback and scoring working

## 🎯 Next Steps

1. **Add Database**: Use free PostgreSQL or MongoDB Atlas for persistence
2. **Add Redis**: For session management (prevents loss on restart)
3. **Add Analytics**: Track usage with Google Analytics
4. **Add Monitoring**: Use Sentry for error tracking
5. **Custom Domain**: Add professional domain name

---

**Need Help?**
- Render Docs: https://render.com/docs
- Check Logs: Render Dashboard → Your Service → Logs
- Discord: https://discord.gg/render

