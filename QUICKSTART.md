# 🚀 Quick Start Guide

## Prerequisites

- Python 3.10+
- Node.js 18+
- Docker & Docker Compose (for Docker deployment)
- OpenRouter API Key ([Get one here](https://openrouter.ai/keys))

## Setup in 3 Steps

### Step 1: Get Your API Key

1. Go to [https://openrouter.ai/keys](https://openrouter.ai/keys)
2. Sign up or log in
3. Create a new API key
4. Copy the key

### Step 2: Choose Your Method

#### Option A: Docker (Easiest) 🐳

```bash
# 1. Set your API key
export OPENROUTER_API_KEY=your_key_here

# 2. Start everything
docker-compose up -d

# 3. Open browser
open http://localhost:3000

# View logs
docker-compose logs -f
```

#### Option B: Manual Development Setup 💻

**Terminal 1 - Backend:**
```bash
cd backend

# Setup
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Configure
echo "OPENROUTER_API_KEY=your_key_here" > .env

# Run
python run.py
```

**Terminal 2 - Frontend:**
```bash
cd frontend

# Setup
npm install

# Configure (optional, defaults to localhost:5000)
echo "VITE_API_URL=http://localhost:5000/api" > .env

# Run
npm run dev
```

**Access:** Open `http://localhost:3000`

### Step 3: Start Interviewing! 🎤

1. Enter a technology (e.g., "Python", "React", "Machine Learning")
2. Enter a position (e.g., "Senior Developer", "Data Scientist")
3. Click "Start Interview"
4. Answer questions and get instant feedback!

## Commands Cheat Sheet

### Docker

```bash
# Start
docker-compose up -d

# Stop
docker-compose down

# Rebuild
docker-compose up --build -d

# Logs
docker-compose logs -f [backend|frontend]

# Restart service
docker-compose restart backend
```

### Development

```bash
# Backend
cd backend
source venv/bin/activate
python run.py

# Frontend
cd frontend
npm run dev

# Build for production
npm run build
```

## Troubleshooting

### "API key not found"
- Check `.env` file exists in `backend/` directory
- Verify `OPENROUTER_API_KEY` is set correctly

### "Backend is not available"
- Backend: Check `http://localhost:5000/health`
- Make sure backend is running (Terminal 1)
- Check no other service is using port 5000

### "Cannot connect to backend"
- Frontend: Check `VITE_API_URL` in `frontend/.env`
- Make sure both backend and frontend are running
- Check CORS settings in `backend/app/__init__.py`

### Docker Issues
```bash
# Reset everything
docker-compose down -v
docker-compose up --build -d

# Check container status
docker-compose ps

# View container logs
docker-compose logs backend
```

## Test the API Directly

```bash
# Health check
curl http://localhost:5000/health

# Create interview
curl -X POST http://localhost:5000/api/interview/create \
  -H "Content-Type: application/json" \
  -d '{"technology":"Python","position":"Senior Developer"}'
```

## Next Steps

- 📖 Read [README_PRODUCTION.md](README_PRODUCTION.md) for architecture details
- 🚀 Check [DEPLOYMENT.md](DEPLOYMENT.md) for production deployment
- 🔧 Explore API endpoints in `backend/app/routes/interview.py`
- 🎨 Customize UI in `frontend/src/components/`

## Getting Help

1. **Check logs:**
   - Docker: `docker-compose logs -f`
   - Backend: Check terminal running `python run.py`
   - Frontend: Check terminal running `npm run dev`

2. **Verify setup:**
   - Backend running on port 5000
   - Frontend running on port 3000
   - API key is valid and has credits

3. **Common fixes:**
   - Restart services
   - Clear browser cache
   - Check environment variables
   - Verify network connectivity

---

**Happy Interviewing! 🎯**

