"""
Seed script to add test donors to the database for testing the matching system.
Run this once to populate the database with sample data.
"""

from datetime import date, timedelta
from app.db.database import SessionLocal
from app.models.donor import Donor
import uuid

def seed_donors():
    db = SessionLocal()
    
    # Clear existing donors
    db.query(Donor).delete()
    db.commit()
    
    # Test donors near Bangalore (latitude: 12.9753, longitude: 77.591)
    test_donors = [
        {
            "name": "Rajesh Kumar",
            "age": 28,
            "blood_group": "O-",
            "latitude": 12.97,
            "longitude": 77.59,
            "contact_number": "9876543210",
            "last_donation_date": date.today() - timedelta(days=120),  # 120 days ago (eligible)
        },
        {
            "name": "Priya Singh",
            "age": 32,
            "blood_group": "O+",
            "latitude": 12.98,
            "longitude": 77.60,
            "contact_number": "9876543211",
            "last_donation_date": date.today() - timedelta(days=100),
        },
        {
            "name": "Amit Patel",
            "age": 35,
            "blood_group": "A-",
            "latitude": 12.96,
            "longitude": 77.58,
            "contact_number": "9876543212",
            "last_donation_date": date.today() - timedelta(days=150),
        },
        {
            "name": "Neha Gupta",
            "age": 26,
            "blood_group": "B+",
            "latitude": 12.99,
            "longitude": 77.61,
            "contact_number": "9876543213",
            "last_donation_date": date.today() - timedelta(days=95),
        },
        {
            "name": "Rohan Verma",
            "age": 40,
            "blood_group": "AB-",
            "latitude": 12.95,
            "longitude": 77.57,
            "contact_number": "9876543214",
            "last_donation_date": date.today() - timedelta(days=110),
        },
        {
            "name": "Aisha Khan",
            "age": 29,
            "blood_group": "O-",
            "latitude": 13.00,
            "longitude": 77.62,
            "contact_number": "9876543215",
            "last_donation_date": date.today() - timedelta(days=130),
        },
        {
            "name": "Vikram Singh",
            "age": 45,
            "blood_group": "A+",
            "latitude": 12.94,
            "longitude": 77.56,
            "contact_number": "9876543216",
            "last_donation_date": date.today() - timedelta(days=105),
        },
        {
            "name": "Sanjana Desai",
            "age": 31,
            "blood_group": "B-",
            "latitude": 13.01,
            "longitude": 77.63,
            "contact_number": "9876543217",
            "last_donation_date": date.today() - timedelta(days=125),
        },
    ]
    
    for donor_data in test_donors:
        donor = Donor(
            id=uuid.uuid4(),
            **donor_data,
            available=True,
            health_eligible=True,
            donation_frequency_6m=2,
            successful_previous_matches=3,
            has_adverse_reactions=False,
        )
        db.add(donor)
    
    db.commit()
    print(f"✅ Successfully seeded {len(test_donors)} test donors!")
    print("\nTest donors added near Bangalore (12.9753, 77.591)")
    for i, donor in enumerate(test_donors, 1):
        print(f"  {i}. {donor['name']} - {donor['blood_group']} - {donor['age']} years")
    
    db.close()

if __name__ == "__main__":
    seed_donors()
