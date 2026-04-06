# Docker Setup Guide for LifeLink

This guide covers building, running, and managing LifeLink using Docker.

## Files Overview

### Docker Files Created

1. **Dockerfile.backend** - Multi-stage build for FastAPI backend
   - Optimized for production with minimal image size
   - Includes health checks
   - Non-root user for security
   - Builds on Python 3.11-slim

2. **Dockerfile.frontend** - Multi-stage build for React frontend
   - Development build with Node 18
   - Production serving with Nginx
   - Gzip compression enabled
   - SPA routing configured

3. **docker-compose.yml** - Orchestrates all services
   - PostgreSQL database
   - FastAPI backend
   - Nginx + React frontend
   - Health checks for all services
   - Environment variable support

4. **nginx.conf** - Nginx configuration
   - SPA routing (try_files fallback)
   - API proxying to backend
   - Gzip compression
   - Cache headers for static assets
   - Security headers

5. **.dockerignore** - Excludes unnecessary files from builds
   - Reduces image size
   - Improves build speed

6. **.env.example** - Environment variables template
   - Copy to `.env` and customize for your environment

7. **docker-compose.override.yml** - Development overrides
   - Enable hot reload
   - Debug mode
   - Volume mounts for live editing

8. **docker.sh** - Helper script for common Docker tasks

---

## Quick Start

### Prerequisites

```bash
# Install Docker Desktop from https://www.docker.com/products/docker-desktop
# Or on Linux:
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
```

### Setup

1. **Clone environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration if needed
   ```

2. **Build images:**
   ```bash
   docker-compose build
   # Or use helper script
   ./docker.sh build
   ```

3. **Start services:**
   ```bash
   docker-compose up -d
   # Or use helper script
   ./docker.sh start
   ```

4. **Access the application:**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Docs: http://localhost:8000/docs

---

## Common Commands

### Using docker-compose directly

```bash
# Start services in foreground (Ctrl+C to stop)
docker-compose up

# Start services in background
docker-compose up -d

# Stop services
docker-compose down

# Stop services and remove volumes
docker-compose down -v

# View logs
docker-compose logs

# View logs for specific service
docker-compose logs backend
docker-compose logs frontend
docker-compose logs database

# Execute command in running container
docker-compose exec backend python -c "import app; print('OK')"

# Rebuild images
docker-compose build --no-cache

# Run migrations
docker-compose exec backend alembic upgrade head

# Seed database
docker-compose exec backend python seed_data.py
```

### Using helper script

```bash
# Build images
./docker.sh build

# Start services
./docker.sh start

# Stop services
./docker.sh stop

# Restart services
./docker.sh restart

# View logs
./docker.sh logs
./docker.sh logs:backend
./docker.sh logs:frontend
./docker.sh logs:database

# Development mode with hot reload
./docker.sh dev

# Run migrations
./docker.sh migrate

# Seed database
./docker.sh seed

# Clean everything
./docker.sh clean

# Check Docker installation
./docker.sh check
```

---

## Development Mode

For local development with hot reload:

```bash
# Option 1: Use helper script
./docker.sh dev

# Option 2: Use docker-compose with override
docker-compose -f docker-compose.yml -f docker-compose.override.yml up
```

This will:
- Enable debug mode on backend
- Enable hot reload for backend Python code changes
- Enable hot reload for frontend
- Mount volumes for live editing
- Run frontend dev server on port 5173

---

## Environment Variables

Configuration is managed via `.env` file:

```env
# Database
DB_USER=lifelink_user
DB_PASSWORD=lifelink_password
DB_NAME=lifelink_db

# Application
APP_ENV=production          # production | development
DEBUG=false                 # true | false
SECRET_KEY=your-secret-key
LOG_LEVEL=info             # debug | info | warning | error

# ML
MODEL_PATH=/app/ml/models

# Frontend
FRONTEND_URL=http://localhost:3000
```

---

## Troubleshooting

### Port Already in Use

If ports 3000, 8000, or 5432 are already in use:

```yaml
# Edit docker-compose.yml and change ports:
ports:
  - "3001:80"      # frontend (external:internal)
  - "8001:8000"    # backend
  - "5433:5432"    # database
```

### Database Connection Issues

```bash
# Check database logs
docker-compose logs database

# Connect to database directly
docker-compose exec database psql -U lifelink_user -d lifelink_db

# Reset database
docker-compose down -v
docker-compose up -d
```

### Backend Not Starting

```bash
# Check backend logs
docker-compose logs backend

# Rebuild without cache
docker-compose build --no-cache backend
docker-compose up backend
```

### Frontend Build Issues

```bash
# Check frontend logs
docker-compose logs frontend

# Rebuild frontend
docker-compose build --no-cache frontend
```

### Health Check Failures

```bash
# View health check logs
docker-compose ps

# Rebuild and restart
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

---

## Performance Optimization

### Image Size Reduction

Current sizes after optimization:
- Backend: ~500MB (Python 3.11-slim + dependencies)
- Frontend: ~50MB (Nginx Alpine + built React app)

To further reduce:
```dockerfile
# Use alpine base images
FROM python:3.11-alpine
FROM node:18-alpine
```

### Build Caching

```bash
# Ensure efficient layer caching
docker-compose build --no-cache  # Full rebuild
docker-compose build             # Uses cache
```

### Multi-stage Builds

Already implemented in both Dockerfiles:
- Reduces final image size
- Separates build dependencies from runtime

---

## Production Deployment

### Docker Hub (Private Registry)

```bash
# Build for production
docker-compose build

# Tag images
docker tag lifelink-backend:latest myregistry/lifelink-backend:v1.0.0
docker tag lifelink-frontend:latest myregistry/lifelink-frontend:v1.0.0

# Push to registry
docker push myregistry/lifelink-backend:v1.0.0
docker push myregistry/lifelink-frontend:v1.0.0
```

### Environment-Specific Configs

Create production overrides:

```yaml
# docker-compose.prod.yml
version: '3.9'

services:
  backend:
    environment:
      DEBUG: "false"
      APP_ENV: production
    restart: always
    deploy:
      replicas: 2
      resources:
        limits:
          cpus: '0.5'
          memory: 512M

  frontend:
    restart: always
```

Run with:
```bash
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

---

## Kubernetes Deployment

Convert to Kubernetes manifests:

```bash
# Install kompose
curl -L https://github.com/kubernetes/kompose/releases/download/v1.28.0/kompose-linux-amd64 -o kompose
chmod +x kompose

# Generate K8s manifests
./kompose convert -f docker-compose.yml -o k8s/
```

---

## Security Considerations

✅ **Implemented Security Features:**

1. **Non-root users** - Services run as unprivileged users
2. **Health checks** - Monitors service availability
3. **Network isolation** - Internal Docker bridge network
4. **Environment variables** - Secrets not in images
5. **Multi-stage builds** - Reduced attack surface
6. **.dockerignore** - Excludes sensitive files

⚠️ **Additional for Production:**

```yaml
# Add to docker-compose.yml for production
services:
  backend:
    security_opt:
      - no-new-privileges:true
    read_only: true
    tmpfs:
      - /tmp
      - /run

  frontend:
    security_opt:
      - no-new-privileges:true
    read_only: true
    tmpfs:
      - /var/run
```

---

## Monitoring & Logging

### View Real-time Metrics

```bash
# Monitor container stats
docker stats

# Watch specific service
docker stats lifelink-backend
```

### Centralized Logging (Optional)

```yaml
# Add ELK stack or similar
# Edit docker-compose.yml
services:
  logstash:
    image: docker.elastic.co/logstash/logstash:7.17.0
    # ... configuration
```

---

## Additional Resources

- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Reference](https://docs.docker.com/compose/compose-file/)
- [FastAPI Deployment](https://fastapi.tiangolo.com/deployment/)
- [Nginx Docker](https://hub.docker.com/_/nginx)
- [PostgreSQL Docker](https://hub.docker.com/_/postgres)

---

## Support

For issues or questions:
1. Check logs: `docker-compose logs [service]`
2. Verify `.env` configuration
3. Ensure Docker daemon is running
4. Check available disk space
5. Review this guide's troubleshooting section
