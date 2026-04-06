#!/bin/bash

# Docker build and development script for LifeLink

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Functions
print_info() {
    echo -e "${BLUE}ℹ ${1}${NC}"
}

print_success() {
    echo -e "${GREEN}✓ ${1}${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ ${1}${NC}"
}

print_error() {
    echo -e "${RED}✗ ${1}${NC}"
}

# Check if Docker is installed
check_docker() {
    if ! command -v docker &> /dev/null; then
        print_error "Docker is not installed"
        exit 1
    fi
    print_success "Docker is installed"
}

# Check if Docker Compose is installed
check_docker_compose() {
    if ! command -v docker-compose &> /dev/null; then
        print_error "Docker Compose is not installed"
        exit 1
    fi
    print_success "Docker Compose is installed"
}

# Build images
build_images() {
    print_info "Building Docker images..."
    docker-compose build
    print_success "Images built successfully"
}

# Start services
start_services() {
    print_info "Starting services..."
    docker-compose up -d
    print_success "Services started"
    print_info "Frontend: http://localhost:3000"
    print_info "Backend API: http://localhost:8000"
    print_info "Database: localhost:5432"
}

# Stop services
stop_services() {
    print_info "Stopping services..."
    docker-compose down
    print_success "Services stopped"
}

# View logs
view_logs() {
    print_info "Viewing logs (Ctrl+C to exit)..."
    docker-compose logs -f
}

# View specific service logs
view_service_logs() {
    if [ -z "$1" ]; then
        print_error "Please specify a service: backend, frontend, or database"
        exit 1
    fi
    print_info "Viewing $1 logs (Ctrl+C to exit)..."
    docker-compose logs -f "$1"
}

# Run migrations
run_migrations() {
    print_info "Running database migrations..."
    docker-compose exec backend alembic upgrade head
    print_success "Migrations completed"
}

# Seed database
seed_database() {
    print_info "Seeding database..."
    docker-compose exec backend python seed_data.py
    print_success "Database seeded"
}

# Clean up
cleanup() {
    print_warning "This will remove all containers, volumes, and networks"
    read -p "Are you sure? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        print_info "Cleaning up..."
        docker-compose down -v
        print_success "Cleanup completed"
    else
        print_info "Cleanup cancelled"
    fi
}

# Dev mode
dev_mode() {
    print_info "Starting in development mode..."
    docker-compose -f docker-compose.yml -f docker-compose.override.yml up
}

# Show usage
show_usage() {
    cat << EOF
LifeLink Docker Management Script

Usage: $0 [command]

Commands:
    build           Build Docker images
    start           Start all services
    stop            Stop all services
    restart         Restart all services
    logs            View logs from all services
    logs:backend    View backend logs
    logs:frontend   View frontend logs
    logs:database   View database logs
    dev             Start in development mode with hot reload
    migrate         Run database migrations
    seed            Seed the database with sample data
    clean           Remove all containers and volumes
    check           Check Docker installation
    help            Show this help message

Examples:
    $0 build
    $0 start
    $0 logs:backend
    $0 dev
EOF
}

# Main script logic
main() {
    case "${1:-help}" in
        build)
            check_docker
            check_docker_compose
            build_images
            ;;
        start)
            check_docker
            check_docker_compose
            start_services
            ;;
        stop)
            check_docker
            check_docker_compose
            stop_services
            ;;
        restart)
            check_docker
            check_docker_compose
            stop_services
            start_services
            ;;
        logs)
            check_docker
            check_docker_compose
            view_logs
            ;;
        logs:*)
            service="${1#logs:}"
            check_docker
            check_docker_compose
            view_service_logs "$service"
            ;;
        dev)
            check_docker
            check_docker_compose
            dev_mode
            ;;
        migrate)
            check_docker
            check_docker_compose
            run_migrations
            ;;
        seed)
            check_docker
            check_docker_compose
            seed_database
            ;;
        clean)
            check_docker
            check_docker_compose
            cleanup
            ;;
        check)
            check_docker
            check_docker_compose
            ;;
        help)
            show_usage
            ;;
        *)
            print_error "Unknown command: $1"
            show_usage
            exit 1
            ;;
    esac
}

main "$@"
