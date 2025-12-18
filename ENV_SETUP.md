# Environment Variables Setup Guide

## Overview

This application uses environment variables for configuration. All sensitive data and configurable settings are stored in `.env` files.

## 📁 Environment Files

### 1. Root `.env` (for Docker Compose)
Location: `/ai-interviewer/.env`

```bash
# Copy example file
cp .env.example .env
```

**Required Variables:**
- `OPENROUTER_API_KEY` - Your OpenRouter API key (required)
- `VITE_API_URL` - Backend API URL for frontend
- `BACKEND_PORT` - Port for backend (default: 5001)
- `FRONTEND_PORT` - Port for frontend (default: 3000)

### 2. Backend `.env`
Location: `/ai-interviewer/backend/.env`

```bash
cd backend
cp .env.example .env
```

**Required Variables:**
- `OPENROUTER_API_KEY` - Your OpenRouter API key

**Optional Variables:**
- `MODEL` - AI model to use (default: mistralai/mistral-small-creative)
- `TEMPERATURE` - Model temperature (default: 0.7)
- `CORS_ORIGINS` - Allowed CORS origins (default: *)
- `SECRET_KEY` - Flask secret key (change in production!)
- `SESSION_TIMEOUT_HOURS` - Session expiry time (default: 2)

### 3. Frontend `.env`
Location: `/ai-interviewer/frontend/.env`

```bash
cd frontend
cp .env.example .env
```

**Required Variables:**
- `VITE_API_URL` - Backend API URL (e.g., http://localhost:5001/api)

**Optional Variables:**
- `VITE_APP_NAME` - Application name
- `VITE_ENABLE_DEBUG` - Enable debug logging

## 🚀 Quick Setup

### For Docker (Recommended):

```bash
# 1. Copy root .env file
cp .env.example .env

# 2. Edit and add your API key
nano .env
# or
code .env

# 3. Set your OPENROUTER_API_KEY
OPENROUTER_API_KEY=your_actual_key_here

# 4. Start Docker
docker-compose up -d
```

### For Local Development:

```bash
# 1. Backend setup
cd backend
cp .env.example .env
# Edit and add OPENROUTER_API_KEY
nano .env

# 2. Frontend setup
cd ../frontend
cp .env.example .env
# Edit VITE_API_URL if needed
nano .env

# 3. Start backend
cd ../backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python run.py

# 4. Start frontend (new terminal)
cd ../frontend
npm install
npm run dev
```

## 🔑 Getting API Keys

### OpenRouter API Key

1. Go to https://openrouter.ai/keys
2. Sign up or log in
3. Click "Create Key"
4. Copy the key
5. Add to your `.env` file:
   ```
   OPENROUTER_API_KEY=sk-or-v1-xxx...
   ```

## 🔒 Security Best Practices

### ❌ Never Do This:
```bash
# DON'T commit .env files
git add .env  # ❌ NO!

# DON'T use default secrets in production
SECRET_KEY=change-me-in-production  # ❌ NO!
```

### ✅ Always Do This:
```bash
# DO use .env.example as template
cp .env.example .env  # ✅ YES!

# DO generate random secrets for production
SECRET_KEY=$(openssl rand -hex 32)  # ✅ YES!

# DO add .env to .gitignore
echo ".env" >> .gitignore  # ✅ YES!
```

## 📝 Environment Variable Reference

### Backend Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `OPENROUTER_API_KEY` | ✅ Yes | - | OpenRouter API key |
| `MODEL` | No | mistralai/mistral-small-creative | AI model name |
| `OPENROUTER_BASE_URL` | No | https://openrouter.ai/api/v1 | API base URL |
| `TEMPERATURE` | No | 0.7 | Model temperature (0.0-1.0) |
| `PORT` | No | 5000 | Backend port |
| `FLASK_ENV` | No | development | Environment (development/production) |
| `FLASK_DEBUG` | No | True | Enable debug mode |
| `SECRET_KEY` | No | auto-generated | Flask secret key |
| `CORS_ORIGINS` | No | * | Allowed CORS origins |
| `SESSION_TIMEOUT_HOURS` | No | 2 | Session expiry time |
| `DEFAULT_QUESTIONS_COUNT` | No | 5 | Default questions per interview |
| `MAX_QUESTIONS_COUNT` | No | 10 | Maximum questions allowed |
| `AGENT_TIMEOUT` | No | 120 | Agent timeout in seconds |

### Frontend Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `VITE_API_URL` | ✅ Yes | http://localhost:5001/api | Backend API URL |
| `VITE_APP_NAME` | No | AI Interviewer | Application name |
| `VITE_APP_DESCRIPTION` | No | Multi-Agent Interview System | App description |
| `VITE_ENABLE_ANALYTICS` | No | false | Enable analytics |
| `VITE_ENABLE_DEBUG` | No | false | Enable debug logging |

### Docker Compose Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `BACKEND_PORT` | No | 5001 | Host port for backend |
| `FRONTEND_PORT` | No | 3000 | Host port for frontend |
| `OPENROUTER_API_KEY` | ✅ Yes | - | OpenRouter API key |
| `VITE_API_URL` | No | http://localhost:5001/api | Frontend API URL |

## 🌍 Environment-Specific Configuration

### Development
```bash
FLASK_ENV=development
FLASK_DEBUG=True
CORS_ORIGINS=*
VITE_ENABLE_DEBUG=true
```

### Production
```bash
FLASK_ENV=production
FLASK_DEBUG=False
SECRET_KEY=<random-string-here>
CORS_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
VITE_ENABLE_DEBUG=false
```

### Testing
```bash
FLASK_ENV=testing
FLASK_DEBUG=True
CORS_ORIGINS=*
```

## 🐛 Troubleshooting

### "OPENROUTER_API_KEY not found"
```bash
# Check if .env file exists
ls -la .env

# Check if variable is set
cat .env | grep OPENROUTER_API_KEY

# Make sure no spaces around =
OPENROUTER_API_KEY=your_key  # ✅ Good
OPENROUTER_API_KEY = your_key  # ❌ Bad (spaces)
```

### "Backend is not available"
```bash
# Check VITE_API_URL in frontend
cat frontend/.env | grep VITE_API_URL

# Should match backend URL
VITE_API_URL=http://localhost:5001/api
```

### Docker not picking up .env changes
```bash
# Rebuild containers
docker-compose down
docker-compose up --build
```

## 📚 Additional Resources

- [Docker Compose Environment Variables](https://docs.docker.com/compose/environment-variables/)
- [Vite Environment Variables](https://vitejs.dev/guide/env-and-mode.html)
- [Flask Configuration](https://flask.palletsprojects.com/en/2.3.x/config/)

## 🆘 Need Help?

1. Check all `.env.example` files for reference
2. Verify API key is valid at https://openrouter.ai/keys
3. Make sure no spaces in `.env` file entries
4. Rebuild Docker containers after .env changes
5. Check logs: `docker-compose logs -f`

