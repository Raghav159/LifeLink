"""
Pytest configuration and shared fixtures
"""
import pytest
import os
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Set test environment
os.environ["DATABASE_URL"] = "sqlite:///:memory:"


@pytest.fixture(scope="session")
def test_db_url():
    """Return test database URL"""
    return "sqlite:///:memory:"


@pytest.fixture
def client():
    """
    Create a test client for FastAPI app.
    This fixture can be used across all tests.
    """
    from app.main import app
    return TestClient(app)
