from sqlalchemy.orm import Session
from app.models.donor import Donor
from app.models.request import BloodRequest
from app.utils.blood_compatibility import is_compatible
from app.utils.distance import haversine_distance
from datetime import date
import uuid


def match_donors(db: Session, request_id: uuid.UUID):
    # Fetch request
    request = db.query(BloodRequest).filter(
        BloodRequest.id == request_id
    ).first()

    if not request:
        return None

    today = date.today()

    # Base filtering (DB-level)
    donors = db.query(Donor).filter(
        Donor.available == True,
        Donor.health_eligible == True,
        Donor.age >= 18,
        Donor.age <= 65
    ).all()

    matched = []

    for donor in donors:

        # 1️⃣ Blood compatibility
        if not is_compatible(donor.blood_group, request.blood_group_required):
            continue

        # 2️⃣ 90-day donation rule
        days_since_last_donation = (today - donor.last_donation_date).days

        if days_since_last_donation < 90:
            continue

        # 3️⃣ Distance calculation
        distance = haversine_distance(
            donor.latitude,
            donor.longitude,
            request.latitude,
            request.longitude
        )

        # 4️⃣ Scoring logic

        # Distance score (closer = better)
        distance_score = 1 / (1 + distance)

        # Urgency weight
        urgency_weights = {
            "LOW": 1,
            "MEDIUM": 2,
            "HIGH": 3
        }

        urgency_score = urgency_weights.get(
            request.urgency_level.value,
            1
        )

        # Recency bonus (longer since last donation = better)
        recency_score = min(days_since_last_donation / 365, 1)

        # Final weighted score
        final_score = (
            (0.5 * distance_score) +
            (0.3 * (urgency_score / 3)) +
            (0.2 * recency_score)
        )

        matched.append({
            "donor_id": donor.id,
            "name": donor.name,
            "blood_group": donor.blood_group,
            "distance_km": round(distance, 2),
            "score": round(final_score, 4)
        })

    # Sort by highest score first
    matched.sort(key=lambda x: x["score"], reverse=True)

    return matched
