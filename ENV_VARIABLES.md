# Environment Variables Reference

Complete list of all environment variables used in the AI Interviewer application.

---

## 🎯 Quick Start Templates

### Local Development (.env)

```bash
# ============================================
# AI Interviewer - Local Development
# ============================================

# === Required ===
OPENROUTER_API_KEY=sk-or-v1-your-actual-api-key-here

# === Backend Configuration ===
FLASK_ENV=development
FLASK_DEBUG=True
PORT=5001
SECRET_KEY=dev-secret-key-change-in-production

# === CORS Configuration ===
# Leave empty or set to "*" for development
CORS_ORIGINS=

# === AI Model Configuration ===
MODEL=mistralai/mistral-small-creative
OPENROUTER_BASE_URL=https://openrouter.ai/api/v1
TEMPERATURE=0.7

# === Interview Settings ===
DEFAULT_QUESTIONS_COUNT=5
MAX_QUESTIONS_COUNT=10
AGENT_TIMEOUT=120
SESSION_TIMEOUT_HOURS=2

# === Docker Configuration ===
BACKEND_PORT=5001
FRONTEND_PORT=3000

# === Frontend Configuration ===
VITE_API_URL=http://localhost:5001/api
VITE_APP_NAME=AI Interviewer
VITE_APP_DESCRIPTION=Multi-Agent Interview System
VITE_ENABLE_ANALYTICS=false
VITE_ENABLE_DEBUG=true

# === Optional (Redis) ===
# REDIS_URL=redis://localhost:6379/0
```

---

### Production - Backend (Render/Railway/Fly.io)

```bash
# ============================================
# AI Interviewer Backend - Production
# ============================================

# === Required ===
OPENROUTER_API_KEY=sk-or-v1-your-actual-production-key
FLASK_ENV=production
FLASK_DEBUG=False
SECRET_KEY=<use: openssl rand -hex 32>
CORS_ORIGINS=https://ai-interviewer-reactjs.vercel.app

# === Server Configuration ===
PORT=10000

# === AI Model Configuration ===
MODEL=mistralai/mistral-small-creative
OPENROUTER_BASE_URL=https://openrouter.ai/api/v1
TEMPERATURE=0.7

# === Interview Settings ===
DEFAULT_QUESTIONS_COUNT=5
MAX_QUESTIONS_COUNT=10
AGENT_TIMEOUT=120
SESSION_TIMEOUT_HOURS=2

# === Optional (Production Database) ===
# REDIS_URL=redis://:password@hostname:port/0
```

---

### Production - Frontend (Vercel/Netlify)

```bash
# ============================================
# AI Interviewer Frontend - Production
# ============================================

# === Required ===
VITE_API_URL=https://ai-interviewer-reactjs.onrender.com/api

# === Optional ===
VITE_APP_NAME=AI Interviewer
VITE_APP_DESCRIPTION=Multi-Agent Interview System powered by AI
VITE_ENABLE_ANALYTICS=false
VITE_ENABLE_DEBUG=false
```

---

## 📋 Complete Variable Reference

### Backend Variables

| Variable | Required | Default | Description | Example |
|----------|----------|---------|-------------|---------|
| **OPENROUTER_API_KEY** | ✅ Yes | None | OpenRouter API key for AI model access | `sk-or-v1-abc123...` |
| **FLASK_ENV** | ✅ Yes (Prod) | `development` | Flask environment mode (controls CORS behavior) | `production` or `development` |
| **FLASK_DEBUG** | No | `True` (dev), `False` (prod) | Enable Flask debug mode | `True` or `False` |
| **PORT** | No | `5001` | Port for backend server | `5001`, `10000` (Render) |
| **SECRET_KEY** | ✅ Yes (Prod) | `dev-secret-key...` | Flask secret key for sessions | `openssl rand -hex 32` |
| **CORS_ORIGINS** | ✅ Yes (Prod) | `*` | Allowed origins for CORS (comma-separated) | `https://frontend.com,https://app.com` |
| **MODEL** | No | `mistralai/mistral-small-creative` | AI model to use via OpenRouter | `mistralai/mistral-small-creative` |
| **OPENROUTER_BASE_URL** | No | `https://openrouter.ai/api/v1` | OpenRouter API base URL | `https://openrouter.ai/api/v1` |
| **TEMPERATURE** | No | `0.7` | AI model temperature (0.0-1.0) | `0.7` |
| **DEFAULT_QUESTIONS_COUNT** | No | `5` | Default number of interview questions | `5` |
| **MAX_QUESTIONS_COUNT** | No | `10` | Maximum allowed questions per interview | `10` |
| **AGENT_TIMEOUT** | No | `120` | Timeout in seconds for AI agent responses | `120` |
| **SESSION_TIMEOUT_HOURS** | No | `2` | Hours before interview session expires | `2` |
| **REDIS_URL** | No | `redis://localhost:6379/0` | Redis connection URL (if using Redis) | `redis://user:pass@host:6379/0` |

---

### Frontend Variables

| Variable | Required | Default | Description | Example |
|----------|----------|---------|-------------|---------|
| **VITE_API_URL** | ✅ Yes (Prod) | `http://localhost:5001/api` | Backend API URL | `https://backend.com/api` |
| **VITE_APP_NAME** | No | `AI Interviewer` | Application name displayed in UI | `AI Interviewer Pro` |
| **VITE_APP_DESCRIPTION** | No | `Multi-Agent Interview System` | App description for SEO/metadata | `Your personal AI interview coach` |
| **VITE_ENABLE_ANALYTICS** | No | `false` | Enable analytics tracking | `true` or `false` |
| **VITE_ENABLE_DEBUG** | No | `false` | Enable debug logging in browser console | `true` or `false` |

---

### Docker Compose Variables

| Variable | Required | Default | Description | Example |
|----------|----------|---------|-------------|---------|
| **BACKEND_PORT** | No | `5001` | Host port mapping for backend | `5001` |
| **FRONTEND_PORT** | No | `3000` | Host port mapping for frontend | `3000` |

---

## 🔐 Security Guidelines

### Development ✅

```bash
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=dev-secret-key-change-in-production  # OK for dev
CORS_ORIGINS=*  # OR leave empty - allows all origins
```

### Production ⚠️

```bash
FLASK_ENV=production  # MUST BE SET!
FLASK_DEBUG=False     # MUST BE False!
SECRET_KEY=<strong-random-key>  # MUST BE UNIQUE!
CORS_ORIGINS=https://yourdomain.com  # MUST BE SPECIFIC!
```

**Generate secure SECRET_KEY:**
```bash
openssl rand -hex 32
# Output: 3a5b2c8d9e0f1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b
```

---

## 🌍 Environment-Specific Configurations

### Local Development (No Docker)

**Terminal 1 - Backend:**
```bash
cd backend
export OPENROUTER_API_KEY=sk-or-v1-your-key
export FLASK_ENV=development
export FLASK_DEBUG=True
python run.py
```

**Terminal 2 - Frontend:**
```bash
cd frontend
export VITE_API_URL=http://localhost:5001/api
npm run dev
```

---

### Docker Development

**Create `.env` in project root:**
```bash
cat > .env << 'EOF'
OPENROUTER_API_KEY=sk-or-v1-your-key
FLASK_ENV=development
FLASK_DEBUG=True
CORS_ORIGINS=*
BACKEND_PORT=5001
FRONTEND_PORT=3000
VITE_API_URL=http://localhost:5001/api
EOF

docker-compose up
```

---

### Production (Render Backend + Vercel Frontend)

**Render Dashboard → Backend Service → Environment:**
```bash
OPENROUTER_API_KEY=sk-or-v1-your-production-key
FLASK_ENV=production
FLASK_DEBUG=False
SECRET_KEY=<generated-32-char-hex>
CORS_ORIGINS=https://ai-interviewer-reactjs.vercel.app
PORT=10000
MODEL=mistralai/mistral-small-creative
TEMPERATURE=0.7
SESSION_TIMEOUT_HOURS=2
```

**Vercel Dashboard → Frontend Project → Settings → Environment Variables:**
```bash
VITE_API_URL=https://ai-interviewer-reactjs.onrender.com/api
VITE_APP_NAME=AI Interviewer
VITE_ENABLE_DEBUG=false
```

---

## ⚙️ Variable Details

### CORS_ORIGINS Behavior

The behavior depends on `FLASK_ENV`:

| FLASK_ENV | CORS_ORIGINS | Actual Behavior |
|-----------|--------------|-----------------|
| `development` | (any value) | Allows `*` (all origins) |
| `production` | (not set) | ⚠️ Allows `*` (UNSAFE!) |
| `production` | `*` | ⚠️ Allows `*` (UNSAFE!) |
| `production` | `https://app.com` | ✅ Allows only that origin |
| `production` | `https://a.com,https://b.com` | ✅ Allows both origins |

**Best Practice for Production:**
```bash
FLASK_ENV=production
CORS_ORIGINS=https://your-frontend.vercel.app
```

---

### AI Model Options

Available models via OpenRouter:

```bash
# Recommended (Fast, Affordable)
MODEL=mistralai/mistral-small-creative

# More Powerful Options
MODEL=mistralai/mistral-medium
MODEL=anthropic/claude-3-sonnet
MODEL=openai/gpt-4
MODEL=openai/gpt-3.5-turbo

# Budget Options
MODEL=mistralai/mistral-7b-instruct
MODEL=meta-llama/llama-3-8b-instruct
```

**Check pricing:** https://openrouter.ai/docs#models

---

### Temperature Values

Controls AI response randomness:

```bash
TEMPERATURE=0.0  # Deterministic, consistent (good for testing)
TEMPERATURE=0.3  # Low creativity (factual answers)
TEMPERATURE=0.7  # Balanced (recommended)
TEMPERATURE=1.0  # High creativity (more varied responses)
TEMPERATURE=1.5  # Very creative (may be unpredictable)
```

---

## 🧪 Testing Configuration

### Test if environment variables are loaded:

**Backend:**
```bash
# Visit: http://localhost:5001/api/test
# or: https://your-backend.onrender.com/api/test

# Check response:
{
  "environment": {
    "flask_env": "production",
    "debug_mode": "False"
  },
  "cors": {
    "mode": "specific origins: ['https://frontend.com']"
  },
  "model": {
    "model": "mistralai/mistral-small-creative",
    "api_key_configured": true
  }
}
```

**Frontend:**
```javascript
// Open browser console on your frontend
console.log(import.meta.env)
// Shows all VITE_ variables
```

---

## 🚨 Common Issues

### Issue 1: "OPENROUTER_API_KEY not found"
```bash
# Backend won't start without this
✅ Fix: Set OPENROUTER_API_KEY in environment variables
```

### Issue 2: "SECRET_KEY must be set in production"
```bash
# Backend raises error if using default key in production
✅ Fix: Set unique SECRET_KEY when FLASK_ENV=production
```

### Issue 3: CORS errors in production
```bash
# Wrong:
CORS_ORIGINS=http://frontend.com  # Frontend is HTTPS!

# Correct:
CORS_ORIGINS=https://frontend.com
```

### Issue 4: Frontend can't connect to backend
```bash
# Wrong:
VITE_API_URL=http://localhost:5001/api  # In production!

# Correct (production):
VITE_API_URL=https://your-backend.onrender.com/api
```

---

## 📚 Platform-Specific Guides

### Render.com

1. Dashboard → Your Service → Environment
2. Click "Add Environment Variable"
3. Enter key-value pairs
4. Click "Save Changes"
5. Service auto-redeploys

**Important:** On Render, use `PORT=10000` (Render's default)

---

### Vercel

1. Dashboard → Your Project → Settings → Environment Variables
2. Add variables (must start with `VITE_` for frontend)
3. Select environment (Production/Preview/Development)
4. Click "Save"
5. Redeploy from Deployments tab

**Important:** Vercel requires redeploy after env var changes!

---

### Railway.app

1. Dashboard → Your Project → Variables
2. Click "New Variable"
3. Enter key-value pairs
4. Changes apply immediately (auto-redeploys)

---

### Fly.io

```bash
# Set variables via CLI
fly secrets set OPENROUTER_API_KEY=sk-or-v1-your-key
fly secrets set FLASK_ENV=production
fly secrets set SECRET_KEY=$(openssl rand -hex 32)
fly secrets set CORS_ORIGINS=https://your-frontend.vercel.app

# View all secrets
fly secrets list
```

---

## ✅ Production Checklist

### Backend Deployment

- [ ] `OPENROUTER_API_KEY` set (valid key)
- [ ] `FLASK_ENV=production`
- [ ] `FLASK_DEBUG=False`
- [ ] `SECRET_KEY` set to unique random value
- [ ] `CORS_ORIGINS` set to exact frontend URL(s)
- [ ] `PORT` set correctly for platform
- [ ] All optional variables set as needed

### Frontend Deployment

- [ ] `VITE_API_URL` set to backend URL with `/api`
- [ ] Backend URL uses `https://` not `http://`
- [ ] No trailing slash in URLs
- [ ] Optional variables set as desired
- [ ] Redeployed after setting variables

### Testing

- [ ] Backend `/health` returns 200
- [ ] Backend `/api/test` shows correct config
- [ ] Frontend loads without errors
- [ ] Can create interview session
- [ ] No CORS errors in browser console

---

**Last Updated:** December 2025  
**Version:** 3.0

