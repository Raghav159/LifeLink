.PHONY: help build start stop restart logs dev migrate seed clean check

help:
	@echo "LifeLink Docker Commands"
	@echo ""
	@echo "Usage: make [command]"
	@echo ""
	@echo "Commands:"
	@echo "  build       Build Docker images"
	@echo "  start       Start all services"
	@echo "  stop        Stop all services"
	@echo "  restart     Restart all services"
	@echo "  logs        View logs from all services"
	@echo "  dev         Start in development mode with hot reload"
	@echo "  migrate     Run database migrations"
	@echo "  seed        Seed the database with sample data"
	@echo "  clean       Remove all containers and volumes"
	@echo "  check       Check Docker installation"
	@echo "  sh          Open backend shell"
	@echo "  db-shell    Open database shell"

build:
	docker-compose build

start:
	docker-compose up -d
	@echo ""
	@echo "LifeLink started successfully!"
	@echo "Frontend:  http://localhost:3000"
	@echo "Backend:   http://localhost:8000"
	@echo "API Docs:  http://localhost:8000/docs"

stop:
	docker-compose down

restart: stop start

logs:
	docker-compose logs -f

logs-backend:
	docker-compose logs -f backend

logs-frontend:
	docker-compose logs -f frontend

logs-database:
	docker-compose logs -f database

dev:
	docker-compose -f docker-compose.yml -f docker-compose.override.yml up

dev-build:
	docker-compose -f docker-compose.yml -f docker-compose.override.yml build

migrate:
	docker-compose exec backend alembic upgrade head

seed:
	docker-compose exec backend python seed_data.py

clean:
	docker-compose down -v
	@echo "All containers and volumes removed"

check:
	@docker --version
	@docker-compose --version
	@echo "Docker is installed and ready!"

sh:
	docker-compose exec backend bash

db-shell:
	docker-compose exec database psql -U lifelink_user -d lifelink_db

test:
	docker-compose exec backend pytest

test-frontend:
	docker-compose exec frontend npm run test

ps:
	docker-compose ps

stats:
	docker stats

pull:
	docker-compose pull

push:
	@echo "Building production images..."
	docker-compose build
	@echo "To push images, run: docker push <image-name>"
