# Port Configuration Guide

## 🔌 Understanding Ports

The application uses **port 5001** consistently across all development environments.

### Local Development (Without Docker)

When running locally with `python run.py`:
- **Backend**: `http://localhost:5001`
- **Frontend**: `http://localhost:3000`
- **Frontend API calls**: Proxied through Vite to backend on port 5001

**Configuration:**
- Backend runs on port 5001 (default in `backend/app/config.py`)
- Frontend config defaults to `http://localhost:5001/api`
- Vite proxy forwards `/api` requests to `http://localhost:5001`

### Docker Development

When running with `docker-compose up`:
- **Backend** (host): `http://localhost:5001` → (container): `5000`
- **Frontend** (host): `http://localhost:3000` → (container): `80`

**Configuration:**
- Docker Compose maps host port 5001 to container port 5000
- Set `VITE_API_URL=http://localhost:5001/api` (or use default)
- Both local and Docker use the same external port (5001)

### Production

**Vercel (Frontend):**
- Served on `https://ai-interviewer-reactjs.vercel.app`
- Set `VITE_API_URL=https://ai-interviewer-reactjs.onrender.com/api`

**Render (Backend):**
- Served on `https://ai-interviewer-reactjs.onrender.com`
- Uses port 10000 internally (Render default)
- Set `CORS_ORIGINS=https://ai-interviewer-reactjs.vercel.app`

## 📋 Quick Setup Guide

### Setup 1: Local Development (No Docker)

```bash
# Backend - Terminal 1
cd backend
pip install -r requirements.txt
python run.py
# Runs on http://localhost:5001

# Frontend - Terminal 2
cd frontend
npm install
npm run dev
# Runs on http://localhost:3000
# API calls proxied to http://localhost:5001
```

**Environment Variables:**
- Backend: Uses default port 5001
- Frontend: Uses default `http://localhost:5001/api` (no env var needed)

### Setup 2: Docker Development

```bash
# Create .env file
cat > .env << 'EOF'
OPENROUTER_API_KEY=your_key_here
BACKEND_PORT=5001
FRONTEND_PORT=3000
VITE_API_URL=http://localhost:5001/api
EOF

# Start services
docker-compose up
```

Access:
- Frontend: http://localhost:3000
- Backend: http://localhost:5001/api
- Backend Health: http://localhost:5001/health

### Setup 3: Production (Vercel + Render)

**Backend on Render:**
```bash
# Environment Variables
OPENROUTER_API_KEY=your_key_here
FLASK_ENV=production
FLASK_DEBUG=False
CORS_ORIGINS=https://ai-interviewer-reactjs.vercel.app
PORT=10000
```

**Frontend on Vercel:**
```bash
# Environment Variables
VITE_API_URL=https://ai-interviewer-reactjs.onrender.com/api
```

## 🐛 Common Issues

### Issue: Port 5001 already in use

**Cause**: Another process is using port 5001

**Fix**:
```bash
# Find and kill the process on port 5001 (macOS/Linux)
lsof -ti:5001 | xargs kill -9

# Or use a different port
PORT=5002 python backend/run.py
# Then update frontend: VITE_API_URL=http://localhost:5002/api
```

### Issue: "Failed to connect to backend"

**Cause**: Backend not running or wrong port

**Fix**:
```bash
# Verify backend is running:
curl http://localhost:5001/health

# Should return: {"status":"healthy","service":"ai-interviewer-backend"}
```

### Issue: "Connection refused" (Docker)

**Cause**: Port mapping incorrect or VITE_API_URL not set

**Fix**:
```bash
# In .env file:
BACKEND_PORT=5001
VITE_API_URL=http://localhost:5001/api

# Rebuild containers:
docker-compose down
docker-compose up --build
```

### Issue: CORS Error (Production)

**Cause**: Backend CORS not configured for frontend origin

**Fix**: On Render backend, set:
```bash
CORS_ORIGINS=https://ai-interviewer-reactjs.vercel.app
```

## 📊 Port Reference Table

| Environment | Backend URL | Frontend URL | Frontend API Config |
|-------------|-------------|--------------|---------------------|
| **Local (No Docker)** | http://localhost:5001 | http://localhost:3000 | http://localhost:5001/api (default) |
| **Docker** | http://localhost:5001 | http://localhost:3000 | http://localhost:5001/api (default) |
| **Production** | https://ai-interviewer-reactjs.onrender.com | https://ai-interviewer-reactjs.vercel.app | https://ai-interviewer-reactjs.onrender.com/api (set via env) |

## 🎯 Key Takeaways

1. **Consistent port 5001**: Both local and Docker development use port 5001
2. **No configuration needed**: Defaults work for both local and Docker
3. **Production**: Use full HTTPS URLs with proper CORS configuration
4. **Always set `VITE_API_URL`** in production deployments
5. **Port 5000 avoided**: Due to macOS conflicts (AirPlay Receiver, etc.)

## ✅ Testing Connectivity

### Test Backend:
```bash
# Local (no Docker) and Docker
curl http://localhost:5001/health

# Production
curl https://ai-interviewer-reactjs.onrender.com/health
```

### Test Frontend → Backend:
```bash
# Open browser console at your frontend URL
fetch('/api/test').then(r => r.json()).then(console.log)
```

Should return backend configuration info without CORS errors.

