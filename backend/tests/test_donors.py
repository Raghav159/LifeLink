"""
Test cases for donor schema validation
"""
import pytest
from pydantic import ValidationError
from app.schemas.donor import DonorCreate


class TestDonorValidation:
    """Test donor schema validation - no database required"""
    
    def test_create_donor_valid(self):
        """Test creating a valid donor object"""
        donor_data = {
            "name": "John Doe",
            "age": 30,
            "blood_group": "O+",
            "latitude": 12.9716,
            "longitude": 77.5946,
            "contact_number": "9876543210",
            "last_donation_date": "2024-01-15",
        }
        donor = DonorCreate(**donor_data)
        assert donor.name == "John Doe"
        assert donor.age == 30
        assert donor.blood_group == "O+"
    
    def test_create_donor_missing_required_field(self):
        """Test that missing required field raises validation error"""
        donor_data = {
            "age": 30,
            "blood_group": "O+",
            "latitude": 12.9716,
            "longitude": 77.5946,
        }
        with pytest.raises(ValidationError):
            DonorCreate(**donor_data)
    
    def test_create_donor_invalid_age(self):
        """Test that negative age raises validation error"""
        donor_data = {
            "name": "Jane Doe",
            "age": -5,
            "blood_group": "A+",
            "latitude": 12.9716,
            "longitude": 77.5946,
            "contact_number": "9876543210",
        }
        with pytest.raises(ValidationError):
            DonorCreate(**donor_data)
