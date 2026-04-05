#!/usr/bin/env python3
"""Seed Neon database with test donors"""
import os
import sys
from datetime import datetime, timedelta
from uuid import uuid4
from dotenv import load_dotenv

# Add the backend directory to path
sys.path.insert(0, os.path.dirname(__file__))

load_dotenv()

from app.models.donor import Donor
from app.db.database import SessionLocal, engine, Base
from sqlalchemy.orm import Session

# Create tables
Base.metadata.create_all(bind=engine)

def seed_donors():
    """Add test donors to database"""
    db = SessionLocal()
    
    try:
        # Check if donors already exist
        existing_count = db.query(Donor).count()
        if existing_count > 0:
            print(f"⚠️  Database already has {existing_count} donors. Skipping seed.")
            return
        
        # Test donors (same as before)
        donors_data = [
            {
                "name": "Rajesh Kumar",
                "age": 28,
                "blood_group": "O-",
                "contact_number": "+91-9876543210",
                "latitude": 12.9716,
                "longitude": 77.5946,
                "available": True,
                "health_eligible": True,
                "last_donation_date": datetime.now() - timedelta(days=120),
                "donation_frequency_6m": 3,
                "successful_previous_matches": 5,
                "has_adverse_reactions": False,
            },
            {
                "name": "Priya Singh",
                "age": 32,
                "blood_group": "O+",
                "contact_number": "+91-9123456789",
                "latitude": 12.9730,
                "longitude": 77.5943,
                "available": True,
                "health_eligible": True,
                "last_donation_date": datetime.now() - timedelta(days=100),
                "donation_frequency_6m": 2,
                "successful_previous_matches": 3,
                "has_adverse_reactions": False,
            },
            {
                "name": "Neha Gupta",
                "age": 26,
                "blood_group": "B+",
                "contact_number": "+91-8765432109",
                "latitude": 12.9720,
                "longitude": 77.5950,
                "available": True,
                "health_eligible": True,
                "last_donation_date": datetime.now() - timedelta(days=110),
                "donation_frequency_6m": 4,
                "successful_previous_matches": 7,
                "has_adverse_reactions": False,
            },
            {
                "name": "Amit Patel",
                "age": 35,
                "blood_group": "A-",
                "contact_number": "+91-7654321098",
                "latitude": 12.9710,
                "longitude": 77.5960,
                "available": True,
                "health_eligible": True,
                "last_donation_date": datetime.now() - timedelta(days=95),
                "donation_frequency_6m": 2,
                "successful_previous_matches": 2,
                "has_adverse_reactions": False,
            },
            {
                "name": "Aisha Khan",
                "age": 29,
                "blood_group": "O-",
                "contact_number": "+91-6543210987",
                "latitude": 12.9725,
                "longitude": 77.5935,
                "available": True,
                "health_eligible": True,
                "last_donation_date": datetime.now() - timedelta(days=105),
                "donation_frequency_6m": 3,
                "successful_previous_matches": 4,
                "has_adverse_reactions": False,
            },
            {
                "name": "Vikram Singh",
                "age": 45,
                "blood_group": "A+",
                "contact_number": "+91-5432109876",
                "latitude": 12.9715,
                "longitude": 77.5925,
                "available": True,
                "health_eligible": True,
                "last_donation_date": datetime.now() - timedelta(days=115),
                "donation_frequency_6m": 1,
                "successful_previous_matches": 1,
                "has_adverse_reactions": False,
            },
        ]
        
        # Add to database
        for donor_data in donors_data:
            donor = Donor(
                id=uuid4(),
                **donor_data
            )
            db.add(donor)
        
        db.commit()
        print(f"✅ Successfully seeded {len(donors_data)} test donors to Neon database!")
        
        # Verify
        count = db.query(Donor).count()
        print(f"📊 Total donors in database: {count}")
        
    except Exception as e:
        print(f"❌ Error seeding database: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    print("🌱 Seeding Neon database with test donors...")
    seed_donors()
