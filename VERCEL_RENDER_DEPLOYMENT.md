# Vercel + Render Deployment Guide

## 🎯 Your Current Setup

- **Frontend (Vercel)**: `https://ai-interviewer-reactjs.vercel.app/`
- **Backend (Render)**: `https://ai-interviewer-reactjs.onrender.com`

## 🚀 Fix CORS Error - Quick Steps

### Step 1: Update Backend CORS on Render

1. Go to https://render.com/dashboard
2. Click on your **backend service** (`ai-interviewer-backend`)
3. Click **"Environment"** tab on the left
4. Find or add `CORS_ORIGINS` variable
5. Set the value to:
   ```
   https://ai-interviewer-reactjs.vercel.app
   ```
   
   **Note**: Remove trailing slash if any, Vercel typically doesn't use it

6. Click **"Save Changes"**
7. Backend will automatically redeploy (takes ~2-3 minutes)

### Step 2: Verify Backend Environment Variables

Make sure these are set on Render:

```bash
OPENROUTER_API_KEY=your_actual_key_here
FLASK_ENV=production
FLASK_DEBUG=False
SECRET_KEY=<generate-random-string>
CORS_ORIGINS=https://ai-interviewer-reactjs.vercel.app
MODEL=mistralai/mistral-small-creative
TEMPERATURE=0.7
SESSION_TIMEOUT_HOURS=2
```

### Step 3: Verify Frontend Environment Variables on Vercel

1. Go to https://vercel.com/dashboard
2. Click on your project
3. Go to **Settings** → **Environment Variables**
4. Make sure these are set:

```bash
VITE_API_URL=https://ai-interviewer-reactjs.onrender.com/api
VITE_APP_NAME=AI Interviewer
VITE_ENABLE_DEBUG=false
```

5. If you changed anything, click **"Redeploy"** from the Deployments tab

## ✅ Test the Fix

### 1. Test Backend Health:
```bash
curl https://ai-interviewer-reactjs.onrender.com/health
```

Should return:
```json
{"status":"healthy","service":"ai-interviewer-backend"}
```

### 2. Test CORS:
```bash
curl -H "Origin: https://ai-interviewer-reactjs.vercel.app" \
     -H "Access-Control-Request-Method: POST" \
     -H "Access-Control-Request-Headers: Content-Type" \
     -X OPTIONS \
     https://ai-interviewer-reactjs.onrender.com/api/interview/create \
     -v
```

Should see in response:
```
Access-Control-Allow-Origin: https://ai-interviewer-reactjs.vercel.app
```

### 3. Test in Browser:

1. Open: https://ai-interviewer-reactjs.vercel.app/
2. Open Browser DevTools (F12) → Console tab
3. Fill in Technology and Position
4. Click "Start Interview"
5. Check if interview starts without CORS errors

## 🔧 Common Issues & Fixes

### Issue 1: Still Getting CORS Error ❌

**Possible causes:**

1. **Trailing slash mismatch**
   ```bash
   # Try both in CORS_ORIGINS (comma-separated):
   CORS_ORIGINS=https://ai-interviewer-reactjs.vercel.app,https://ai-interviewer-reactjs.vercel.app/
   ```

2. **Browser cache**
   - Hard refresh: `Ctrl+Shift+R` (Windows) or `Cmd+Shift+R` (Mac)
   - Or open in Incognito mode

3. **Backend not redeployed**
   - Check Render dashboard → Logs
   - Look for "Starting server" message
   - Wait until status is "Live"

### Issue 2: Backend Returns 502 ❌

**Cause**: Render free tier apps sleep after 15 minutes

**Fix**: 
1. First request takes ~30-60 seconds (cold start)
2. Keep backend awake with UptimeRobot:
   - Sign up at https://uptimerobot.com (free)
   - Add monitor: `https://ai-interviewer-reactjs.onrender.com/health`
   - Check interval: every 5 minutes

### Issue 3: Environment Variables Not Applied ❌

**Render**:
1. After changing env vars, backend auto-redeploys
2. Check **"Events"** tab to see deployment status
3. Wait for "Deploy succeeded" message

**Vercel**:
1. After changing env vars, you must **manually redeploy**
2. Go to **"Deployments"** tab
3. Click "⋯" on latest deployment → "Redeploy"

## 🔍 Debug Mode

### Enable Debug Logging on Backend:

Temporarily set on Render:
```bash
FLASK_DEBUG=True
FLASK_ENV=development
```

Then check Render logs for detailed CORS information.

**Remember to disable after debugging!**

## 📊 Free Tier Limits

### Vercel (Frontend):
- ✅ 100GB bandwidth/month
- ✅ Instant deployments
- ✅ Automatic HTTPS
- ✅ Global CDN
- ✅ Unlimited personal projects

### Render (Backend):
- ✅ 750 hours/month free compute
- ✅ Auto-sleep after 15 min inactivity
- ✅ Cold start: ~30-60 seconds
- ✅ 100GB bandwidth/month
- ✅ Free SSL certificates
- ⚠️ Logs retained for 7 days

## 🔒 Security Checklist

- [x] `OPENROUTER_API_KEY` set as environment variable on Render
- [x] `SECRET_KEY` changed from default
- [x] `FLASK_DEBUG=False` in production
- [x] `CORS_ORIGINS` set to specific Vercel URL
- [x] HTTPS enabled (automatic on both platforms)
- [x] `.env` files not committed to Git

## 🚀 Auto-Deploy Setup

### Vercel (Frontend):
- Automatically deploys on Git push to `main`
- Or deploy manually: `vercel --prod`

### Render (Backend):
- Automatically deploys on Git push to `main`
- Can also trigger manual deploy from dashboard

## 📱 Custom Domain (Optional)

### On Vercel (Frontend):
1. Go to **Settings** → **Domains**
2. Add your domain: `interview.yourdomain.com`
3. Follow DNS instructions
4. After setup, update backend CORS:
   ```bash
   CORS_ORIGINS=https://interview.yourdomain.com
   ```

### On Render (Backend):
1. Go to **Settings** → **Custom Domain**
2. Add: `api.yourdomain.com`
3. Update Vercel env:
   ```bash
   VITE_API_URL=https://api.yourdomain.com/api
   ```

## 🆘 Quick Troubleshooting Commands

```bash
# 1. Test backend is alive
curl https://ai-interviewer-reactjs.onrender.com/health

# 2. Test CORS headers
curl -I -H "Origin: https://ai-interviewer-reactjs.vercel.app" \
  https://ai-interviewer-reactjs.onrender.com/api/interview/create

# 3. Test create interview endpoint
curl -X POST https://ai-interviewer-reactjs.onrender.com/api/interview/create \
  -H "Content-Type: application/json" \
  -H "Origin: https://ai-interviewer-reactjs.vercel.app" \
  -d '{"technology":"Python","position":"Developer"}' \
  -v
```

## 🎯 Current Status Checklist

After making changes, verify:

- [ ] Backend environment `CORS_ORIGINS` includes Vercel URL
- [ ] Backend deployed successfully (check Render "Events")
- [ ] Frontend environment `VITE_API_URL` points to Render backend
- [ ] Frontend redeployed after env changes
- [ ] Backend `/health` endpoint returns 200
- [ ] CORS headers include Vercel origin
- [ ] Frontend loads without errors
- [ ] Can create interview session
- [ ] Can start interview without CORS error

## 📞 Still Having Issues?

1. **Check Browser Console** (F12):
   - Look for exact error message
   - Check Network tab → Failed request → Headers

2. **Check Render Logs**:
   - Go to backend service → Logs tab
   - Look for CORS or error messages

3. **Verify URLs match exactly**:
   - No extra `/` at the end
   - `https` not `http`
   - Correct subdomain

4. **Common mistakes**:
   - Forgetting to redeploy on Vercel after env changes
   - Typo in environment variable names
   - Using `http` instead of `https`
   - Including port numbers (not needed for deployed apps)

---

**Need More Help?**
- Vercel Docs: https://vercel.com/docs
- Render Docs: https://render.com/docs
- Check deployment logs on both platforms

