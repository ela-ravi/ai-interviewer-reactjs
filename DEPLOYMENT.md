# Deployment Guide

## Project Structure

```
ai-interviewer/
├── backend/              # Flask API
│   ├── app/             # Application code
│   ├── agents.py        # Autogen agents
│   ├── run.py           # Entry point
│   ├── requirements.txt # Python dependencies
│   └── Dockerfile       # Backend container
├── frontend/            # React UI
│   ├── src/            # React components
│   ├── package.json    # Node dependencies
│   ├── Dockerfile      # Frontend container
│   └── nginx.conf      # Nginx configuration
└── docker-compose.yml  # Docker orchestration
```

## Development Setup

### Backend

```bash
cd backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env
# Edit .env and add your OPENROUTER_API_KEY

# Run development server
python run.py
```

Backend will be available at `http://localhost:5000`

### Frontend

```bash
cd frontend

# Install dependencies
npm install

# Create .env file
cp .env.example .env

# Run development server
npm run dev
```

Frontend will be available at `http://localhost:3000`

## Docker Deployment

### Quick Start

```bash
# Set your API key
export OPENROUTER_API_KEY=your_key_here

# Build and start all services
docker-compose up --build

# Run in background
docker-compose up -d
```

Access the application at `http://localhost:3000`

### Production Deployment

1. **Set environment variables:**

```bash
# Create .env file in root directory
cat > .env << EOF
OPENROUTER_API_KEY=your_actual_key
SECRET_KEY=$(openssl rand -hex 32)
EOF
```

2. **Build production images:**

```bash
docker-compose build
```

3. **Start services:**

```bash
docker-compose up -d
```

4. **View logs:**

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend
docker-compose logs -f frontend
```

5. **Stop services:**

```bash
docker-compose down
```

## Health Checks

- Backend: `http://localhost:5000/health`
- Frontend: `http://localhost:3000`

## API Endpoints

### Interview Endpoints

- `POST /api/interview/create` - Create new interview session
- `POST /api/interview/{session_id}/start` - Start interview
- `POST /api/interview/{session_id}/answer` - Submit answer
- `POST /api/interview/{session_id}/next-question` - Get next question
- `POST /api/interview/{session_id}/end` - End interview
- `GET /api/interview/{session_id}` - Get session info
- `DELETE /api/interview/{session_id}` - Delete session

## Production Considerations

### Security

1. **Change default secret key:**
   ```bash
   export SECRET_KEY=$(openssl rand -hex 32)
   ```

2. **Use HTTPS:**
   - Set up SSL/TLS certificates
   - Configure reverse proxy (nginx/Apache)

3. **Environment variables:**
   - Never commit `.env` files
   - Use secrets management (AWS Secrets Manager, HashiCorp Vault)

4. **API Key protection:**
   - Keep `OPENROUTER_API_KEY` secure
   - Rotate keys periodically

### Scalability

1. **Use proper WSGI server:**
   - Already using Gunicorn in Docker
   - Configure workers based on CPU cores

2. **Add caching:**
   - Redis for session storage
   - Response caching

3. **Load balancing:**
   - Use nginx/HAProxy
   - Deploy multiple backend instances

4. **Database:**
   - Add PostgreSQL/MongoDB for persistence
   - Store interview history

### Monitoring

1. **Application logs:**
   ```bash
   docker-compose logs -f --tail=100
   ```

2. **Health monitoring:**
   - Set up health check endpoints
   - Use monitoring tools (Prometheus, Grafana)

3. **Error tracking:**
   - Integrate Sentry or similar

## Cloud Deployment

### AWS

```bash
# Using ECS or EKS
# 1. Build and push images to ECR
# 2. Create ECS task definitions
# 3. Set up ALB
# 4. Configure auto-scaling
```

### Google Cloud

```bash
# Using Cloud Run
gcloud builds submit --tag gcr.io/PROJECT_ID/ai-interviewer-backend backend/
gcloud builds submit --tag gcr.io/PROJECT_ID/ai-interviewer-frontend frontend/

gcloud run deploy backend --image gcr.io/PROJECT_ID/ai-interviewer-backend
gcloud run deploy frontend --image gcr.io/PROJECT_ID/ai-interviewer-frontend
```

### Heroku

```bash
# Backend
cd backend
heroku create ai-interviewer-backend
git push heroku main

# Frontend
cd frontend
# Use Heroku buildpack for static sites
```

## Troubleshooting

### Backend not starting

1. Check API key is set:
   ```bash
   docker-compose exec backend env | grep OPENROUTER_API_KEY
   ```

2. View logs:
   ```bash
   docker-compose logs backend
   ```

### Frontend can't connect to backend

1. Check CORS settings in backend
2. Verify API_URL in frontend `.env`
3. Check network connectivity

### Permission errors

```bash
# Fix ownership
sudo chown -R $USER:$USER .

# Fix permissions
chmod -R 755 .
```

## Backup and Recovery

### Session Data

```bash
# If using Redis for sessions
docker exec -it redis redis-cli BGSAVE
```

### Database Backup

```bash
# If using PostgreSQL
docker exec -it postgres pg_dump -U user database > backup.sql
```

## Performance Optimization

1. **Enable caching** at nginx level
2. **Optimize images** and assets
3. **Use CDN** for static files
4. **Enable compression** (gzip/brotli)
5. **Minimize bundle size** in frontend

## Support

For issues, check:
- Application logs
- Health check endpoints
- Environment variables
- Network connectivity
- API key validity

