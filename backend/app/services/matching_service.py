import logging
from datetime import date
from typing import List
from uuid import UUID

import numpy as np
from sqlalchemy.orm import Session

from app.models.donor import Donor
from app.models.request import BloodRequest
from app.schemas.matching import DonorMatchResult
from app.utils.blood_compatibility import is_compatible
from app.utils.distance import haversine_distance

logger = logging.getLogger(__name__)


def check_eligibility(donor: Donor, request: BloodRequest) -> bool:
    """
    Check if donor is eligible for matching with request.
    
    Criteria:
    - available == True
    - health_eligible == True
    - 18 <= age <= 65
    - blood_group compatible
    - days_since_donation >= 90
    - distance <= 10km
    """
    today = date.today()
    days_since = (today - donor.last_donation_date).days
    distance = haversine_distance(
        donor.latitude, donor.longitude,
        request.latitude, request.longitude
    )
    
    eligible = (
        donor.available and
        donor.health_eligible and
        18 <= donor.age <= 65 and
        is_compatible(donor.blood_group, getattr(request, 'blood_group_required', request.blood_group_required)) and
        days_since >= 90 and
        distance <= 10
    )
    
    return eligible


def compute_features(donor: Donor, request: BloodRequest) -> np.ndarray:
    """
    Compute feature vector for ML prediction (14 features).
    
    Order:
    0. distance_km
    1. days_since_donation
    2. age
    3. is_universal_donor
    4. donation_frequency_6m
    5. successful_previous_matches
    6. has_adverse_reactions
    7. urgency_numeric
    8. quantity_ml
    9. patient_age
    10. request_hour
    11. age_compatibility
    12. distance_urgency_score
    13. recency_urgency_score
    """
    today = date.today()
    distance = haversine_distance(
        donor.latitude, donor.longitude,
        request.latitude, request.longitude
    )
    days_since = (today - donor.last_donation_date).days
    
    urgency_map = {"LOW": 1, "MEDIUM": 2, "HIGH": 3}
    urgency_numeric = urgency_map.get(
        getattr(request.urgency_level, 'value', request.urgency_level),
        1
    )
    
    # Donor features
    is_universal = 1 if donor.blood_group == "O-" else 0
    
    # Interaction features
    age_compat = abs(donor.age - request.patient_age)
    dist_urgency = distance / urgency_numeric if urgency_numeric > 0 else 0
    recency_urgency = days_since * urgency_numeric
    
    features = np.array([[
        distance,
        days_since,
        donor.age,
        is_universal,
        getattr(donor, 'donation_frequency_6m', 0),
        getattr(donor, 'successful_previous_matches', 0),
        int(getattr(donor, 'has_adverse_reactions', False)),
        urgency_numeric,
        request.quantity,
        request.patient_age,
        request.request_hour,
        age_compat,
        dist_urgency,
        recency_urgency
    ]])
    
    return features


def match_donors(
    db: Session,
    request_id: UUID,
    ml_model=None
) -> List[DonorMatchResult]:
    """
    Full matching pipeline with ML ranking:
    1. Fetch request
    2. Get all donors
    3. Filter eligible
    4. Compute features + predict ml_score
    5. Sort by ml_score descending
    6. Return top 20 matches
    """
    logger.info(f"Starting donor matching for request {request_id}...")
    
    # 1. Fetch request
    request = db.query(BloodRequest).filter(BloodRequest.id == request_id).first()
    if not request:
        logger.warning(f"Request {request_id} not found")
        return None
    
    logger.info(f"Request found: blood_group={request.blood_group_required}, urgency={request.urgency_level}")
    
    # 2. Get all donors
    donors = db.query(Donor).all()
    logger.info(f"Total donors in DB: {len(donors)}")
    
    # 3-4. Filter + score
    results = []
    eligible_count = 0
    
    for donor in donors:
        if not check_eligibility(donor, request):
            continue
        
        eligible_count += 1
        
        # Compute features for ML prediction
        features = compute_features(donor, request)
        
        # Get ML score if model available
        ml_score = 0.5  # Default fallback score
        if ml_model is not None:
            try:
                ml_score = float(ml_model.predict_proba(features)[0, 1])
            except Exception as e:
                logger.warning(f"Error computing ML score for donor {donor.id}: {e}")
                ml_score = 0.5
        
        distance = haversine_distance(
            donor.latitude, donor.longitude,
            request.latitude, request.longitude
        )
        
        result = DonorMatchResult(
            donor_id=donor.id,
            name=donor.name,
            blood_group=donor.blood_group,
            distance_km=round(distance, 2),
            ml_score=round(ml_score, 4)
        )
        results.append(result)
    
    logger.info(f"Eligible donors: {eligible_count}")
    
    # 5. Sort by ml_score descending
    results.sort(key=lambda x: x.ml_score, reverse=True)
    
    # Return top 20
    top_results = results[:20]
    logger.info(f"Returning top {len(top_results)} matches")
    
    return top_results
