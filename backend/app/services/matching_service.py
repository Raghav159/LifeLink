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
            age=donor.age,
            blood_group=donor.blood_group,
            contact_number=donor.contact_number,
            latitude=donor.latitude,
            longitude=donor.longitude,
            distance_km=round(distance, 2),
            ml_score=round(ml_score, 4),
            last_donation_date=donor.last_donation_date.isoformat() if donor.last_donation_date else None,
            health_eligible=donor.health_eligible,
            available=donor.available,
            donation_frequency_6m=donor.donation_frequency_6m,
            successful_previous_matches=donor.successful_previous_matches,
            has_adverse_reactions=donor.has_adverse_reactions
        )
        results.append(result)
    
    logger.info(f"Eligible donors: {eligible_count}")
    
    # 5. Calculate combined ranking score (70% ML score + 30% distance proximity)
    # Normalize distance to 0-1 scale (0 is closest, 1 is farthest)
    if results:
        max_distance = max(r.distance_km for r in results) if results else 10
        
        # Create list of (result, combined_score) tuples for sorting
        scored_results = []
        for result in results:
            # Distance score: 1.0 = closest, 0.0 = farthest
            distance_score = 1.0 - (result.distance_km / max(max_distance, 10))
            
            # Combined ranking: prioritize ML score but also consider proximity
            # 70% weight to ML score, 30% weight to distance proximity
            combined_score = (result.ml_score * 0.70) + (distance_score * 0.30)
            
            scored_results.append((result, combined_score))
            logger.debug(f"Donor {result.name}: ML={result.ml_score:.2f}, Distance={result.distance_km}km, "
                        f"DistScore={distance_score:.2f}, Combined={combined_score:.3f}")
        
        # Sort by combined score (best matches first)
        scored_results.sort(key=lambda x: x[1], reverse=True)
        results = [item[0] for item in scored_results]
    
    # Return top 20
    top_results = results[:20]
    logger.info(f"Returning top {len(top_results)} matches")
    
    return top_results
