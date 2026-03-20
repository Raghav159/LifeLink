import numpy as np
from typing import Tuple


def generate_synthetic_data(n_samples: int = 10000, random_state: int = 42) -> Tuple[np.ndarray, np.ndarray]:
    """
    Generate 10,000 synthetic donor-request pairs with realistic distributions.
    
    Features (14 total):
    - Donor Features (7): distance, days_since_donation, age, is_universal_donor,
                         donation_frequency_6m, successful_previous_matches, has_adverse_reactions
    - Request Features (4): urgency_numeric, quantity, patient_age, request_hour
    - Interaction Features (3): age_compatibility, distance_urgency_score, recency_urgency_score
    
    Returns:
        X: shape (n_samples, 14) — feature matrix
        y: shape (n_samples,) — binary labels (0 or 1)
    """
    np.random.seed(random_state)
    
    data = []
    
    for _ in range(n_samples):
        # Donor Features
        distance_km = np.random.exponential(scale=8)
        if distance_km > 10:
            distance_km = 10 + np.random.exponential(1)
        
        days_since_donation = int(np.random.gamma(shape=3, scale=40))
        age = int(np.random.normal(40, 15))
        age = np.clip(age, 18, 65)
        
        is_universal_donor = 1 if np.random.rand() < 0.15 else 0  # 15% O-
        donation_frequency_6m = int(np.random.poisson(lam=2))
        successful_previous_matches = int(np.random.beta(5, 2) * 20)
        has_adverse_reactions = 1 if np.random.rand() < 0.05 else 0
        
        # Request Features
        urgency_numeric = np.random.choice([1, 2, 3], p=[0.3, 0.5, 0.2])
        quantity_ml = int(np.random.normal(450, 50))
        quantity_ml = np.clip(quantity_ml, 300, 600)
        patient_age = int(np.random.normal(40, 20))
        patient_age = np.clip(patient_age, 1, 100)
        request_hour = np.random.randint(0, 24)
        
        # Interaction Features
        age_compatibility = abs(age - patient_age)
        distance_urgency_score = distance_km / urgency_numeric
        recency_urgency_score = days_since_donation * urgency_numeric
        
        features = [
            distance_km, days_since_donation, age, is_universal_donor,
            donation_frequency_6m, successful_previous_matches, has_adverse_reactions,
            urgency_numeric, quantity_ml, patient_age, request_hour,
            age_compatibility, distance_urgency_score, recency_urgency_score
        ]
        
        data.append(features)
    
    # Create labels: 75% positive, 25% negative
    y = np.random.choice([0, 1], size=n_samples, p=[0.25, 0.75])
    
    # Apply domain logic: bad combinations → label 0
    X = np.array(data)
    for i in range(n_samples):
        if X[i, 0] > 10:  # distance > 10km
            y[i] = 0
        if X[i, 1] < 90:  # days_since_donation < 90
            y[i] = 0
        if X[i, 12] > 10:  # distance_urgency_score > 10
            y[i] = 0
    
    return X, y
