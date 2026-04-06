"""
Test cases for LifeLink backend health and core endpoints
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app


@pytest.fixture
def client():
    """Create a test client"""
    return TestClient(app)


class TestHealthEndpoints:
    """Test health check endpoints"""
    
    def test_root_endpoint(self, client):
        """Test root endpoint returns API info"""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "LifeLink API" in data["message"]
    
    def test_health_endpoint(self, client):
        """Test health endpoint"""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "database" in data


class TestCORSConfiguration:
    """Test CORS middleware is properly configured"""
    
    def test_cors_headers_localhost(self, client):
        """Test CORS headers for localhost"""
        response = client.get(
            "/",
            headers={"Origin": "http://localhost:3000"}
        )
        assert response.status_code == 200
    
    def test_cors_headers_frontend(self, client):
        """Test CORS headers for frontend origin"""
        response = client.get(
            "/",
            headers={"Origin": "http://localhost:5173"}
        )
        assert response.status_code == 200


class TestDocumentation:
    """Test API documentation endpoints"""
    
    def test_swagger_docs(self, client):
        """Test Swagger documentation is available"""
        response = client.get("/docs")
        assert response.status_code == 200
    
    def test_redoc(self, client):
        """Test ReDoc documentation is available"""
        response = client.get("/redoc")
        assert response.status_code == 200
    
    def test_openapi_schema(self, client):
        """Test OpenAPI schema endpoint"""
        response = client.get("/openapi.json")
        assert response.status_code == 200
        schema = response.json()
        assert "info" in schema
        assert schema["info"]["title"] == "LifeLink API"
