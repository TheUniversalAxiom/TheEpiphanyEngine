# Deployment Guide

This guide covers deploying the Epiphany Engine in various environments.

## Table of Contents

- [Quick Start](#quick-start)
- [Docker Deployment](#docker-deployment)
- [Production Deployment](#production-deployment)
- [Configuration](#configuration)
- [Security](#security)
- [Monitoring](#monitoring)
- [Troubleshooting](#troubleshooting)

---

## Quick Start

### Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run web API
uvicorn web.api:app --reload

# Access at http://localhost:8000
```

### Docker (Recommended)

```bash
# Build and run with Docker Compose
docker-compose up -d

# Access at http://localhost:8000
```

---

## Docker Deployment

### Building the Image

```bash
# Build the Docker image
docker build -t epiphany-engine:latest .

# Tag for registry (optional)
docker tag epiphany-engine:latest your-registry.com/epiphany-engine:latest

# Push to registry
docker push your-registry.com/epiphany-engine:latest
```

### Running with Docker

**Basic run:**
```bash
docker run -p 8000:8000 epiphany-engine:latest
```

**With environment variables:**
```bash
docker run -p 8000:8000 \
  -e API_KEY_ENABLED=true \
  -e API_KEY=your-secret-key \
  -e LOG_LEVEL=INFO \
  epiphany-engine:latest
```

**With volume mounts (development):**
```bash
docker run -p 8000:8000 \
  -v $(pwd)/axiom:/app/axiom \
  -v $(pwd)/engine:/app/engine \
  -v $(pwd)/web:/app/web \
  epiphany-engine:latest
```

### Docker Compose

**Start services:**
```bash
docker-compose up -d
```

**View logs:**
```bash
docker-compose logs -f web
```

**Stop services:**
```bash
docker-compose down
```

**Rebuild and restart:**
```bash
docker-compose up -d --build
```

---

## Production Deployment

### Requirements

- Python 3.9+
- 1GB RAM minimum (2GB+ recommended)
- 1 CPU core minimum (2+ recommended)
- 500MB disk space

### Environment Setup

1. **Create virtual environment:**
```bash
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# OR
venv\Scripts\activate  # Windows
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Set environment variables:**
```bash
export API_KEY_ENABLED=true
export API_KEY=your-strong-random-key
export JWT_SECRET_KEY=your-jwt-secret
export LOG_LEVEL=INFO
export LOG_FORMAT=json
```

### Running with Uvicorn

**Development:**
```bash
uvicorn web.api:app --reload
```

**Production:**
```bash
uvicorn web.api:app \
  --host 0.0.0.0 \
  --port 8000 \
  --workers 4 \
  --log-level info \
  --access-log
```

### Running with Gunicorn

For production, use Gunicorn with Uvicorn workers:

```bash
pip install gunicorn

gunicorn web.api:app \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000 \
  --log-level info \
  --access-logfile - \
  --error-logfile -
```

### Systemd Service

Create `/etc/systemd/system/epiphany-engine.service`:

```ini
[Unit]
Description=Epiphany Engine API
After=network.target

[Service]
Type=notify
User=epiphany
Group=epiphany
WorkingDirectory=/opt/epiphany-engine
Environment="PATH=/opt/epiphany-engine/venv/bin"
Environment="API_KEY_ENABLED=true"
Environment="API_KEY=your-secret-key"
Environment="LOG_LEVEL=INFO"
ExecStart=/opt/epiphany-engine/venv/bin/gunicorn web.api:app \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000
Restart=always

[Install]
WantedBy=multi-user.target
```

**Enable and start:**
```bash
sudo systemctl daemon-reload
sudo systemctl enable epiphany-engine
sudo systemctl start epiphany-engine
sudo systemctl status epiphany-engine
```

### Reverse Proxy (Nginx)

Create `/etc/nginx/sites-available/epiphany-engine`:

```nginx
server {
    listen 80;
    server_name your-domain.com;

    # Redirect HTTP to HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name your-domain.com;

    # SSL certificates
    ssl_certificate /etc/letsencrypt/live/your-domain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/your-domain.com/privkey.pem;

    # SSL configuration
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;

    # Proxy to Epiphany Engine
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        # WebSocket support (if needed)
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }

    # Rate limiting
    limit_req_zone $binary_remote_addr zone=api:10m rate=10r/s;
    limit_req zone=api burst=20 nodelay;

    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
}
```

**Enable site:**
```bash
sudo ln -s /etc/nginx/sites-available/epiphany-engine /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

---

## Configuration

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `API_KEY_ENABLED` | `false` | Enable API key authentication |
| `API_KEY` | `""` | API key for authentication (X-API-Key header) |
| `JWT_SECRET_KEY` | `"your-secret-key-change-in-production"` | Secret key for JWT tokens |
| `JWT_EXPIRATION_MINUTES` | `60` | JWT token expiration time |
| `LOG_LEVEL` | `INFO` | Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL) |
| `LOG_FORMAT` | `json` | Log format (`json` or `simple`) |

### Docker Compose Configuration

Edit `docker-compose.yml`:

```yaml
services:
  web:
    environment:
      - API_KEY_ENABLED=true
      - API_KEY=your-secret-key-here
      - LOG_LEVEL=INFO
      - LOG_FORMAT=json
    ports:
      - "8000:8000"  # Change port if needed
```

---

## Security

### Authentication Setup

**1. Enable API key authentication:**
```bash
export API_KEY_ENABLED=true
export API_KEY=$(openssl rand -hex 32)
```

**2. Use the API key in requests:**
```bash
curl -H "X-API-Key: your-api-key" http://localhost:8000/api/simulate
```

### Security Checklist

- ✅ **Enable authentication** in production
- ✅ **Use strong API keys** (32+ random characters)
- ✅ **Enable HTTPS** with valid SSL certificates
- ✅ **Keep dependencies updated** (`pip-audit`)
- ✅ **Use rate limiting** (via Nginx or API)
- ✅ **Monitor logs** for suspicious activity
- ✅ **Run as non-root user** in production
- ✅ **Use environment variables** for secrets (never commit)
- ✅ **Enable firewall** rules
- ✅ **Regular security audits**

### Generating Secrets

```bash
# Generate API key
openssl rand -hex 32

# Generate JWT secret
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

---

## Monitoring

### Health Checks

**Endpoint:** `GET /api/health`

```bash
curl http://localhost:8000/api/health
```

**Response:**
```json
{
  "status": "healthy",
  "service": "epiphany-engine",
  "version": "0.1.0",
  "auth_enabled": true
}
```

### Logging

**Structured JSON logs:**
```bash
export LOG_FORMAT=json
```

**Simple logs (development):**
```bash
export LOG_FORMAT=simple
```

**View logs:**
```bash
# Systemd service
sudo journalctl -u epiphany-engine -f

# Docker
docker logs -f epiphany-engine-web

# Docker Compose
docker-compose logs -f web
```

### Monitoring Tools

**Prometheus metrics (future enhancement):**
- Request count and latency
- Simulation execution time
- Error rates

**Log aggregation:**
- Use ELK stack (Elasticsearch, Logstash, Kibana)
- Or Loki + Grafana
- Or cloud services (CloudWatch, Datadog)

---

## Troubleshooting

### Common Issues

**1. Port already in use:**
```bash
# Find process using port 8000
lsof -i :8000
# Kill process or change port
```

**2. Permission denied:**
```bash
# Run as root or add user to docker group
sudo usermod -aG docker $USER
# Re-login for changes to take effect
```

**3. Module not found:**
```bash
# Ensure dependencies are installed
pip install -r requirements.txt

# Check PYTHONPATH
export PYTHONPATH=/path/to/TheEpiphanyEngine
```

**4. Authentication errors:**
```bash
# Verify API key is set
echo $API_KEY

# Check header format
curl -H "X-API-Key: your-key" http://localhost:8000/api/info
```

### Debug Mode

**Enable debug logging:**
```bash
export LOG_LEVEL=DEBUG
```

**Run with verbose output:**
```bash
uvicorn web.api:app --reload --log-level debug
```

### Performance Issues

**1. Increase workers:**
```bash
gunicorn web.api:app --workers 8 --worker-class uvicorn.workers.UvicornWorker
```

**2. Enable caching (future enhancement):**
- Redis for result caching
- CDN for static assets

**3. Database connection pooling (if DB added):**
- Configure connection pool size
- Use connection pooling middleware

---

## Cloud Deployment

### AWS (Elastic Beanstalk)

1. Install EB CLI: `pip install awsebcli`
2. Initialize: `eb init -p python-3.11 epiphany-engine`
3. Create environment: `eb create epiphany-prod`
4. Deploy: `eb deploy`

### Google Cloud (Cloud Run)

```bash
# Build and push to GCR
gcloud builds submit --tag gcr.io/PROJECT_ID/epiphany-engine

# Deploy to Cloud Run
gcloud run deploy epiphany-engine \
  --image gcr.io/PROJECT_ID/epiphany-engine \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

### Kubernetes

See `k8s/` directory for Kubernetes manifests (future addition).

---

## Scaling

### Horizontal Scaling

**Docker Swarm:**
```bash
docker stack deploy -c docker-compose.yml epiphany
```

**Kubernetes:**
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: epiphany-engine
spec:
  replicas: 3
  selector:
    matchLabels:
      app: epiphany-engine
  template:
    metadata:
      labels:
        app: epiphany-engine
    spec:
      containers:
      - name: web
        image: epiphany-engine:latest
        ports:
        - containerPort: 8000
```

### Load Balancing

- Use Nginx/HAProxy for load balancing
- Or cloud load balancers (ALB, Cloud Load Balancer)
- Configure health checks on `/api/health`

---

## Backup and Recovery

### Configuration Backup

```bash
# Backup environment variables
env | grep -E '(API_KEY|JWT|LOG)' > .env.backup

# Secure the backup
chmod 600 .env.backup
```

### Future: Database Backups

When database is added:
- Automated daily backups
- Point-in-time recovery
- Off-site backup storage

---

## Support

For deployment issues:

1. Check [GitHub Issues](https://github.com/TheUniversalAxiom/TheEpiphanyEngine/issues)
2. Review logs for error messages
3. Consult the [CONTRIBUTING.md](CONTRIBUTING.md) guide
4. Open a new issue with deployment details

---

**Last Updated:** 2026-01-10
**Version:** 0.1.0
