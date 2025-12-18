# AI Interviewer - Production Version

Multi-module AI interview application with Flask backend and React frontend.

## 🏗️ Architecture

```
┌─────────────────────────────────────────┐
│         React Frontend (Port 3000)      │
│  ┌────────────────────────────────────┐ │
│  │ - Interview Setup                   │ │
│  │ - Question Display                  │ │
│  │ - Answer Submission                 │ │
│  │ - Feedback & Scoring UI             │ │
│  │ - Summary Dashboard                 │ │
│  └────────────────────────────────────┘ │
└──────────────┬──────────────────────────┘
               │ HTTP/REST API
               ▼
┌─────────────────────────────────────────┐
│         Flask Backend (Port 5000)       │
│  ┌────────────────────────────────────┐ │
│  │ REST API Endpoints                  │ │
│  │ - Session Management                │ │
│  │ - Question Generation               │ │
│  │ - Answer Processing                 │ │
│  └────────────────────────────────────┘ │
│  ┌────────────────────────────────────┐ │
│  │ Autogen Multi-Agent System          │ │
│  │ - Interviewer Agent                 │ │
│  │ - Coach Agent                       │ │
│  │ - Scorer Agent                      │ │
│  └────────────────────────────────────┘ │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│   Mistral AI via OpenRouter             │
└─────────────────────────────────────────┘
```

## 🚀 Quick Start

### Option 1: Docker (Recommended)

```bash
# 1. Set your API key
export OPENROUTER_API_KEY=your_key_here

# 2. Start all services
docker-compose up -d

# 3. Access the application
open http://localhost:3000
```

### Option 2: Manual Setup

**Backend:**
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Add your OPENROUTER_API_KEY to .env
python run.py
```

**Frontend:**
```bash
cd frontend
npm install
cp .env.example .env
npm run dev
```

## 📁 Project Structure

```
ai-interviewer/
├── backend/                    # Flask API Server
│   ├── app/
│   │   ├── __init__.py        # Flask app factory
│   │   ├── config.py          # Configuration
│   │   ├── routes/
│   │   │   └── interview.py   # API endpoints
│   │   └── services/
│   │       └── interview_service.py  # Business logic
│   ├── agents.py              # Autogen agents
│   ├── run.py                 # Entry point
│   ├── requirements.txt       # Python dependencies
│   └── Dockerfile
│
├── frontend/                   # React Application
│   ├── src/
│   │   ├── components/        # React components
│   │   │   ├── InterviewSetup.jsx
│   │   │   ├── Interview.jsx
│   │   │   ├── QuestionCard.jsx
│   │   │   ├── AnswerForm.jsx
│   │   │   ├── FeedbackCard.jsx
│   │   │   └── Summary.jsx
│   │   ├── services/
│   │   │   └── api.js         # API client
│   │   ├── App.jsx            # Main component
│   │   └── main.jsx           # Entry point
│   ├── package.json
│   ├── vite.config.js
│   ├── Dockerfile
│   └── nginx.conf
│
├── docker-compose.yml          # Docker orchestration
├── DEPLOYMENT.md              # Deployment guide
└── README_PRODUCTION.md       # This file
```

## 🔌 API Endpoints

### Session Management

- **POST** `/api/interview/create`
  - Create new interview session
  - Body: `{ "technology": "Python", "position": "Senior Dev" }`
  - Returns: `{ "session_id": "uuid", ... }`

- **GET** `/api/interview/{session_id}`
  - Get session information
  - Returns: Session details and statistics

- **DELETE** `/api/interview/{session_id}`
  - Delete a session

### Interview Flow

- **POST** `/api/interview/{session_id}/start`
  - Start interview and get first question

- **POST** `/api/interview/{session_id}/answer`
  - Submit answer
  - Body: `{ "answer": "..." }`
  - Returns: Feedback and score

- **POST** `/api/interview/{session_id}/next-question`
  - Get next question

- **POST** `/api/interview/{session_id}/end`
  - End interview and get summary

## 🎯 Features

### Multi-Agent System

1. **Interviewer Agent**
   - Generates contextual technical questions
   - Adapts to candidate's level
   - Asks follow-up questions

2. **Coach Agent**
   - Analyzes answers
   - Provides constructive feedback
   - Suggests improvements

3. **Scorer Agent**
   - Evaluates on 0-10 scale
   - Considers multiple factors
   - Provides detailed justification

### Frontend Features

- ✅ Modern React UI with Vite
- ✅ Responsive design
- ✅ Real-time feedback
- ✅ Progress tracking
- ✅ Comprehensive summary
- ✅ Beautiful animations

### Backend Features

- ✅ RESTful API architecture
- ✅ Session management
- ✅ Async agent operations
- ✅ CORS support
- ✅ Error handling
- ✅ Health checks

## 🔧 Configuration

### Backend (.env)

```env
OPENROUTER_API_KEY=your_key_here
SECRET_KEY=your_secret_key
FLASK_ENV=production
CORS_ORIGINS=http://localhost:3000
```

### Frontend (.env)

```env
VITE_API_URL=http://localhost:5000/api
```

## 🐳 Docker Commands

```bash
# Build images
docker-compose build

# Start services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Restart a service
docker-compose restart backend

# Execute command in container
docker-compose exec backend python -c "print('Hello')"
```

## 🧪 Testing

```bash
# Backend
cd backend
pytest

# Frontend
cd frontend
npm run test

# API testing
curl http://localhost:5000/health
```

## 📊 Monitoring

- Backend health: `http://localhost:5000/health`
- Frontend: `http://localhost:3000`
- Logs: `docker-compose logs -f`

## 🔒 Security Best Practices

1. ✅ **Never commit `.env` files**
2. ✅ **Use strong SECRET_KEY** (generate with `openssl rand -hex 32`)
3. ✅ **Keep API keys secure**
4. ✅ **Enable HTTPS** in production
5. ✅ **Implement rate limiting**
6. ✅ **Validate all inputs**
7. ✅ **Use environment-specific configs**

## 🚀 Deployment

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed deployment instructions for:
- AWS (ECS, EKS, Lambda)
- Google Cloud (Cloud Run, GKE)
- Azure (Container Instances, AKS)
- Heroku
- Digital Ocean
- Self-hosted servers

## 📈 Scaling

### Horizontal Scaling

```bash
# Scale backend instances
docker-compose up -d --scale backend=3

# Add load balancer (nginx/HAProxy)
```

### Vertical Scaling

- Increase Gunicorn workers
- Allocate more CPU/RAM to containers
- Optimize database queries

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| Backend won't start | Check `OPENROUTER_API_KEY` is set |
| CORS errors | Verify `CORS_ORIGINS` in backend `.env` |
| Frontend can't connect | Check `VITE_API_URL` matches backend |
| Slow responses | Increase Gunicorn workers |
| Memory issues | Add Redis for session storage |

## 📝 Development Workflow

1. **Create feature branch**
   ```bash
   git checkout -b feature/my-feature
   ```

2. **Make changes**
   - Backend: Test with `python run.py`
   - Frontend: Test with `npm run dev`

3. **Test changes**
   ```bash
   docker-compose up --build
   ```

4. **Commit and push**
   ```bash
   git add .
   git commit -m "feat: add new feature"
   git push origin feature/my-feature
   ```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

MIT License - see LICENSE file for details

## 🙏 Acknowledgments

- **Mistral AI** - LLM provider
- **OpenRouter** - API gateway
- **Microsoft AutoGen** - Multi-agent framework
- **Flask** - Backend framework
- **React** - Frontend framework
- **Vite** - Build tool

## 📧 Support

For issues or questions:
- Check [DEPLOYMENT.md](DEPLOYMENT.md)
- Review API documentation
- Check Docker logs
- Verify environment variables

---

**Built with ❤️ using Flask, React, and AutoGen**

