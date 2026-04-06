"""
Test cases for donor endpoints and services
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from app.main import app
from app.db.database import Base, get_db
from app.models.donor import Donor
import uuid


# Use in-memory SQLite for testing
SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    SQLALCHEMY_TEST_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    """Override get_db dependency for testing"""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


@pytest.fixture(scope="function")
def db():
    """Create test database"""
    Base.metadata.create_all(bind=engine)
    yield TestingSessionLocal()
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client(db):
    """Create test client with overridden database"""
    app.dependency_overrides[get_db] = override_get_db
    return TestClient(app)


@pytest.fixture(autouse=True)
def cleanup():
    """Cleanup after each test"""
    yield
    app.dependency_overrides.clear()


class TestDonorEndpoints:
    """Test donor API endpoints"""
    
    def test_list_donors_empty(self, client):
        """Test listing donors when database is empty"""
        response = client.get("/donors/")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
    
    def test_create_donor(self, client):
        """Test creating a new donor"""
        donor_data = {
            "name": "John Doe",
            "blood_group": "O+",
            "age": 30,
            "latitude": 12.9716,
            "longitude": 77.5946,
            "contact_number": "9876543210",
            "last_donation_date": "2024-01-15"
        }
        response = client.post("/donors/", json=donor_data)
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "John Doe"
        assert data["blood_group"] == "O+"
        assert "id" in data
    
    def test_create_donor_invalid_blood_group(self, client):
        """Test creating donor with invalid blood group"""
        donor_data = {
            "name": "Jane Doe",
            "blood_group": "XX",  # Invalid
            "age": 25,
            "latitude": 12.9716,
            "longitude": 77.5946,
            "contact_number": "9876543210",
            "last_donation_date": "2024-01-15"
        }
        # This should fail validation or server error
        response = client.post("/donors/", json=donor_data)
        assert response.status_code in [422, 400, 500]  # Validation error
    
    def test_get_non_existent_donor(self, client):
        """Test retrieving non-existent donor"""
        fake_id = str(uuid.uuid4())
        response = client.get(f"/donors/{fake_id}")
        assert response.status_code == 404
        data = response.json()
        assert "not found" in data.get("detail", "").lower()
    
    def test_list_donors_after_creation(self, client):
        """Test listing donors after creating one"""
        # Create a donor
        donor_data = {
            "name": "Alice Smith",
            "blood_group": "A+",
            "age": 28,
            "latitude": 12.9716,
            "longitude": 77.5946,
            "contact_number": "9123456789",
            "last_donation_date": "2024-02-01"
        }
        create_response = client.post("/donors/", json=donor_data)
        assert create_response.status_code == 200
        
        # List all donors
        list_response = client.get("/donors/")
        assert list_response.status_code == 200
        data = list_response.json()
        assert len(data) >= 1
        assert any(d["name"] == "Alice Smith" for d in data)


class TestDonorValidation:
    """Test donor data validation"""
    
    def test_create_donor_missing_required_field(self, client):
        """Test creating donor with missing required field"""
        donor_data = {
            "name": "Bob",
            # Missing blood_group
            "age": 35,
            "latitude": 12.9716,
            "longitude": 77.5946,
            "contact_number": "9999999999",
            "last_donation_date": "2024-01-01"
        }
        response = client.post("/donors/", json=donor_data)
        assert response.status_code == 422  # Validation error
    
    def test_create_donor_invalid_age(self, client):
        """Test creating donor with invalid age"""
        donor_data = {
            "name": "Young Person",
            "blood_group": "B-",
            "age": -5,  # Invalid
            "latitude": 12.9716,
            "longitude": 77.5946,
            "contact_number": "9999999999",
            "last_donation_date": "2024-01-01"
        }
        response = client.post("/donors/", json=donor_data)
        # Should fail validation
        assert response.status_code in [422, 400]
