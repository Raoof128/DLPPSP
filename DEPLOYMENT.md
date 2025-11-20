# DLP Platform - Deployment Guide

## 🚀 Quick Deployment Options

### Option 1: Local Development (Recommended for Testing)

```bash
# 1. Clone or navigate to the project
cd dlp_platform

# 2. Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the dashboard
streamlit run dashboard/app.py
# Access at: http://localhost:8501

# OR run the API server
python api/server.py
# Access at: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

### Option 2: Docker Compose (Recommended for Demo)

```bash
# Start both services
docker-compose up --build

# Services available at:
# - Dashboard: http://localhost:8501
# - API:       http://localhost:8000
# - API Docs:  http://localhost:8000/docs

# Stop services
docker-compose down
```

### Option 3: Quick Start Script

```bash
# Make executable (first time only)
chmod +x run.sh

# Run the script
./run.sh

# Choose:
# 1) Streamlit Dashboard
# 2) FastAPI Server
# 3) Run Tests
# 4) Docker Compose
```

## 🐳 Docker Details

### Build Individual Services

```bash
# Build API service
docker build -f Dockerfile.api -t dlp-platform-api .

# Build Dashboard service
docker build -f Dockerfile.dashboard -t dlp-platform-dashboard .

# Run API
docker run -p 8000:8000 dlp-platform-api

# Run Dashboard
docker run -p 8501:8501 dlp-platform-dashboard
```

### Environment Variables

The platform uses minimal configuration. All settings are in:
- `config/patterns_au.json` - PII patterns
- `config/policies.yaml` - DLP policies

No environment variables required for basic operation.

## 📦 Production Deployment (Advanced)

⚠️ **Warning:** This platform is a demonstration tool. For production:

### 1. Security Hardening

```bash
# Add authentication (example with OAuth2)
pip install python-jose passlib

# Enable HTTPS
# - Use reverse proxy (nginx, Traefik)
# - Configure SSL certificates
# - Update CORS settings in api/server.py
```

### 2. Database Integration

```python
# Replace file-based logging with PostgreSQL/MongoDB
pip install sqlalchemy psycopg2-binary
# or
pip install pymongo
```

### 3. Secrets Management

```bash
# Use environment variables for sensitive config
export DLP_SECRET_KEY="your-secret-key"
export DATABASE_URL="postgresql://..."

# Or use cloud secrets manager
# - AWS Secrets Manager
# - Azure Key Vault
# - HashiCorp Vault
```

### 4. Kubernetes Deployment (Example)

```yaml
# deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: dlp-platform-api
spec:
  replicas: 3
  selector:
    matchLabels:
      app: dlp-api
  template:
    metadata:
      labels:
        app: dlp-api
    spec:
      containers:
      - name: api
        image: dlp-platform-api:1.0.0
        ports:
        - containerPort: 8000
        env:
        - name: LOG_LEVEL
          value: "INFO"
---
apiVersion: v1
kind: Service
metadata:
  name: dlp-api-service
spec:
  selector:
    app: dlp-api
  ports:
  - port: 80
    targetPort: 8000
  type: LoadBalancer
```

### 5. Monitoring & Logging

```bash
# Add structured logging
pip install python-json-logger

# Integrate with monitoring
# - Prometheus metrics
# - Grafana dashboards
# - ELK stack for logs
# - Sentry for error tracking
```

## 🧪 Testing Before Deployment

### Run Full Test Suite

```bash
# Unit tests
python -m unittest discover tests -v

# Integration tests (if added)
pytest tests/integration/

# Load testing (example)
pip install locust
locust -f tests/load/locustfile.py
```

### Verify Services

```bash
# Check API health
curl http://localhost:8000/health

# Test email simulation
curl -X POST http://localhost:8000/simulate/email \
  -H "Content-Type: application/json" \
  -d '{"sender":"test@example.com","recipient":"user@example.com","subject":"Test","body":"Clean content"}'

# Verify dashboard loads
# Visit: http://localhost:8501
```

## 📊 Performance Optimization

### For High Volume

```python
# Add caching
pip install redis
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

# Add rate limiting
from slowapi import Limiter
from slowapi.util import get_remote_address

# Add async processing
import asyncio
from concurrent.futures import ThreadPoolExecutor
```

### Database Persistence

```python
# Replace file quarantine with S3/Azure Blob
import boto3
# or
from azure.storage.blob import BlobServiceClient
```

## 🔐 Security Checklist

Before any production deployment:

- [ ] Enable HTTPS/TLS
- [ ] Add authentication (OAuth2, JWT)
- [ ] Implement rate limiting
- [ ] Add request validation and sanitization
- [ ] Enable CORS properly (not `allow_origins=["*"]`)
- [ ] Use secrets manager for credentials
- [ ] Enable audit logging to immutable storage
- [ ] Set up intrusion detection
- [ ] Configure WAF (Web Application Firewall)
- [ ] Implement data encryption at rest
- [ ] Add monitoring and alerting
- [ ] Conduct penetration testing
- [ ] Review code with security team
- [ ] Update dependencies regularly
- [ ] Implement backup and recovery

## 📱 Cloud Platform Specific

### AWS

```bash
# Deploy to ECS
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <account>.dkr.ecr.us-east-1.amazonaws.com
docker tag dlp-platform-api:latest <account>.dkr.ecr.us-east-1.amazonaws.com/dlp-api:latest
docker push <account>.dkr.ecr.us-east-1.amazonaws.com/dlp-api:latest

# Or use App Runner
aws apprunner create-service --cli-input-json file://apprunner.json
```

### Azure

```bash
# Deploy to Container Apps
az containerapp up \
  --name dlp-platform \
  --resource-group dlp-rg \
  --image dlp-platform-api:latest \
  --target-port 8000
```

### GCP

```bash
# Deploy to Cloud Run
gcloud run deploy dlp-platform \
  --image gcr.io/PROJECT_ID/dlp-api:latest \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

## 🌐 Reverse Proxy Setup

### Nginx Configuration

```nginx
server {
    listen 80;
    server_name dlp.example.com;

    location /api/ {
        proxy_pass http://localhost:8000/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location / {
        proxy_pass http://localhost:8501/;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
```

## 📈 Scaling Considerations

### Horizontal Scaling

```yaml
# docker-compose.yml with replicas
services:
  api:
    image: dlp-platform-api
    deploy:
      replicas: 3
    ports:
      - "8000-8002:8000"
```

### Load Balancing

```bash
# Use HAProxy, nginx, or cloud load balancer
# Distribute traffic across multiple API instances
```

## 🆘 Troubleshooting

### Common Issues

**Port Already in Use**
```bash
# Find process
lsof -ti:8000 | xargs kill

# Or change port
uvicorn api.server:app --port 8001
```

**Module Not Found**
```bash
# Ensure virtual environment is activated
source venv/bin/activate
pip install -r requirements.txt
```

**Config File Not Found**
```bash
# Run from project root
cd /path/to/dlp_platform
python api/server.py
```

## 📞 Support

For deployment issues:
- Review logs: `docker logs <container_id>`
- Check health endpoint: `curl http://localhost:8000/health`
- Verify configs: Review `config/` directory
- See troubleshooting: `QUICKSTART.md`

---

**🛡️ DLP Platform - Ready to Deploy**

*Remember: This is a demonstration platform. See SECURITY.md before production use.*
