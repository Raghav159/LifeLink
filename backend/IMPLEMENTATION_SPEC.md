# 🩸 LifeLink Backend — Complete Implementation Specification

**Status**: Ready for Implementation | **Date**: March 20, 2026

---

## Table of Contents
1. [Objective](#objective)
2. [Tech Stack](#tech-stack)
3. [Project Structure](#project-structure)
4. [Environment Configuration](#environment-configuration)
5. [Database Models](#database-models)
6. [Business Logic Requirements](#business-logic-requirements)
7. [ML Model Architecture (XGBoost)](#ml-model-architecture-xgboost)
8. [Services Layer](#services-layer)
9. [API Routes](#api-routes)
10. [Implementation Phases](#implementation-phases)
11. [Verification Checklist](#verification-checklist)

---

## Objective

Build a FastAPI-based blood donor matching platform that:

- Manages donors and blood requests
- Applies real-world medical eligibility rules
- Generates synthetic training data and trains an **XGBoost classifier** (90%+ accuracy)
- Computes geographic proximity and filters by 10km threshold
- **Ranks donors probabilistically** via ML model
- Returns ranked donor results via REST API

**Local deployment** with modular architecture for future ML/DevOps extensions.

---

## Tech Stack

| Component | Technology |
|-----------|-----------|
| **API Framework** | FastAPI |
| **ASGI Server** | Uvicorn |
| **Database** | PostgreSQL |
| **ORM** | SQLAlchemy |
| **Data Validation** | Pydantic |
| **ML Framework** | XGBoost, scikit-learn |
| **Model Persistence** | Joblib |
| **Web CORS** | Starlette CORS middleware |

---

## Project Structure

```
backend/
├── .env
├── requirements.txt
├── config.py
└── app/
    ├── main.py
    ├── core/
    │   └── config.py (enums, constants, logger)
    ├── db/
    │   ├── database.py
    │   └── dependency.py
    ├── models/
    │   ├── __init__.py
    │   ├── donor.py (SQLAlchemy ORM)
    │   └── request.py (SQLAlchemy ORM)
    ├── schemas/
    │   ├── __init__.py
    │   ├── donor.py (Pydantic request/response)
    │   ├── request.py (Pydantic request/response)
    │   └── matching.py (Pydantic response)
    ├── routers/
    │   ├── __init__.py
    │   ├── donor.py
    │   ├── request.py
    │   └── match.py
    ├── services/
    │   ├── __init__.py
    │   ├── donor_service.py
    │   ├── request_service.py
    │   └── matching_service.py
    ├── utils/
    │   ├── __init__.py
    │   ├── blood_compatibility.py
    │   └── distance.py
    └── ml/
        ├── data_generation.py
        ├── train.py
        ├── metrics/
        │   └── model_v1_metrics.json (training logs)
        └── models/
            └── model_v1.pkl (trained model)
```

---

## Environment Configuration

### .env File (Required)

```env
# Database
DATABASE_URL=postgresql://postgres:postgres@127.0.0.1:5432/lifelink

# Application
APP_ENV=development
DEBUG=True
SECRET_KEY=dev-secret-key

# ML Model
MODEL_PATH=app/ml/models/model_v1.pkl

# API Server
API_HOST=127.0.0.1
API_PORT=8000

# Logging
LOG_LEVEL=info

# CORS
FRONTEND_URL=http://localhost:3000
```

### config.py (Pydantic BaseSettings)

Load all env vars into a centralized config class:

```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    APP_ENV: str
    MODEL_PATH: str
    API_HOST: str
    API_PORT: int
    LOG_LEVEL: str
    FRONTEND_URL: str
    
    class Config:
        env_file = ".env"

settings = Settings()
```

---

## Database Models

### Donor Model (SQLAlchemy)

```python
# models/donor.py

class Donor(Base):
    __tablename__ = "donors"
    
    id: UUID = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name: str = Column(String(100), nullable=False)
    age: int = Column(Integer, nullable=False)  # 18-65
    blood_group: str = Column(String(5), nullable=False)  # O-, O+, A-, A+, B-, B+, AB-, AB+
    latitude: float = Column(Float, nullable=False)  # [-90, 90]
    longitude: float = Column(Float, nullable=False)  # [-180, 180]
    available: bool = Column(Boolean, default=True)
    last_donation_date: date = Column(Date, nullable=False)
    contact_number: str = Column(String(20), nullable=False)
    health_eligible: bool = Column(Boolean, default=True)
    donation_frequency_6m: int = Column(Integer, default=0)  # count in last 6 months
    successful_previous_matches: int = Column(Integer, default=0)
    has_adverse_reactions: bool = Column(Boolean, default=False)
```

### BloodRequest Model (SQLAlchemy)

```python
# models/request.py

class BloodRequest(Base):
    __tablename__ = "blood_requests"
    
    id: UUID = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    blood_group_required: str = Column(String(5), nullable=False)  # O-, O+, A-, A+, B-, B+, AB-, AB+
    latitude: float = Column(Float, nullable=False)
    longitude: float = Column(Float, nullable=False)
    urgency_level: str = Column(String(10), nullable=False)  # LOW, MEDIUM, HIGH
    quantity: int = Column(Integer, nullable=False)  # in mL
    patient_age: int = Column(Integer, nullable=False)  # for compatibility
    request_hour: int = Column(Integer, nullable=False)  # 0-23
    created_at: datetime = Column(DateTime, default=datetime.utcnow)
```

---

## Business Logic Requirements

### 5.1 Blood Compatibility Rules

```python
# utils/blood_compatibility.py

def is_compatible(donor_group: str, recipient_group: str) -> bool:
    """
    Donor group → Recipient groups mapping
    - O- → all (universal donor)
    - O+ → O+, A+, B+, AB+
    - A- → A-, AB-
    - A+ → A+, AB+
    - B- → B-, AB-
    - B+ → B+, AB+
    - AB- → AB-
    - AB+ → AB+ (universal recipient)
    """
    compatibility_map = {
        "O-": ["O-", "O+", "A-", "A+", "B-", "B+", "AB-", "AB+"],
        "O+": ["O+", "A+", "B+", "AB+"],
        # ... (complete mapping)
    }
    return recipient_group in compatibility_map.get(donor_group, [])
```

### 5.2 Distance Calculation (Haversine)

```python
# utils/distance.py

import math

def haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Calculate distance between two coordinates in kilometers.
    
    Args:
        lat1, lon1: Donor coordinates
        lat2, lon2: Request coordinates
    
    Returns:
        Distance in km (float)
    """
    R = 6371  # Earth radius in km
    φ1, φ2 = math.radians(lat1), math.radians(lat2)
    Δφ = math.radians(lat2 - lat1)
    Δλ = math.radians(lon2 - lon1)
    
    a = math.sin(Δφ/2)**2 + math.cos(φ1) * math.cos(φ2) * math.sin(Δλ/2)**2
    c = 2 * math.asin(math.sqrt(a))
    
    return R * c
```

### 5.3 Donor Eligibility Rules

A donor is eligible for matching **if and only if**:

1. ✓ `available == True`
2. ✓ `health_eligible == True`
3. ✓ `18 ≤ age ≤ 65`
4. ✓ `blood_group` is compatible
5. ✓ `(today - last_donation_date) ≥ 90 days`
6. ✓ `distance ≤ 10 km` (10km threshold)

---

## ML Model Architecture (XGBoost)

### Overview

**Binary Classification**: Predict whether a donor-request pair will result in a successful match.

- **Framework**: XGBoost
- **Training Data**: 10,000 synthetic donor-request pairs
- **Target Metrics**: Precision ≥ 90%, Recall ≥ 85%, F1 ≥ 0.87, Accuracy 90%+
- **Output**: Probability score [0.0, 1.0]

---

### Feature Engineering (14 Features Total)

#### Donor Features (7)

| Feature | Type | Source | Example |
|---------|------|--------|---------|
| `distance_km` | float | Haversine | 5.2 |
| `days_since_donation` | int | days_between(today, last_donation_date) | 120 |
| `age` | int | Donor.age | 35 |
| `is_universal_donor` | int | 1 if O-, else 0 | 1 |
| `donation_frequency_6m` | int | Donor.donation_frequency_6m | 3 |
| `successful_previous_matches` | int | Donor.successful_previous_matches | 5 |
| `has_adverse_reactions` | int | 0 if no, 1 if yes | 0 |

#### Request Features (4)

| Feature | Type | Source | Example |
|---------|------|--------|---------|
| `urgency_numeric` | int | LOW=1, MEDIUM=2, HIGH=3 | 2 |
| `quantity_ml` | int | BloodRequest.quantity | 450 |
| `patient_age` | int | BloodRequest.patient_age | 45 |
| `request_hour` | int | BloodRequest.request_hour (0-23) | 14 |

#### Interaction Features (3) — *These drive 90%+ accuracy*

| Feature | Formula | Intuition |
|---------|---------|-----------|
| `age_compatibility` | abs(donor_age - patient_age) | Closer ages → safer transfusion |
| `distance_urgency_score` | distance_km / urgency_numeric | Far + urgent = bad combo |
| `recency_urgency_score` | days_since_donation * urgency_numeric | Stale blood + urgent = risky |

---

### Data Generation Pipeline

```python
# ml/data_generation.py

def generate_synthetic_data(n_samples: int = 10000) -> Tuple[np.ndarray, np.ndarray]:
    """
    Generate 10,000 synthetic donor-request pairs with realistic distributions.
    
    Returns:
        X: shape (10000, 14) — features
        y: shape (10000,) — binary labels (0 or 1)
    """
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
    
    # Labels: 75% positive, 25% negative
    y = np.random.choice([0, 1], size=n_samples, p=[0.25, 0.75])
    
    # Add some logic: bad combinations → label 0
    X = np.array(data)
    for i in range(n_samples):
        if X[i, 0] > 10:  # distance > 10km
            y[i] = 0
        if X[i, 1] < 90:  # days_since_donation < 90
            y[i] = 0
        if X[i, 12] > 10:  # distance_urgency_score > 10
            y[i] = 0
    
    return X, y
```

---

### Training Pipeline

```python
# ml/train.py

from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from xgboost import XGBClassifier
import joblib
import json

def train_model(model_path: str = "app/ml/models/model_v1.pkl") -> XGBClassifier:
    """
    Full ML training pipeline:
    1. Generate 10,000 synthetic pairs
    2. Train/val/test split (80/10/10)
    3. Hyperparameter tuning via GridSearch
    4. Train final model on train+val
    5. Evaluate on test set
    6. Save model + metrics
    """
    
    # 1. Generate data
    X, y = generate_synthetic_data(n_samples=10000)
    
    # 2. Stratified split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.1, stratify=y, random_state=42
    )
    X_train, X_val, y_train, y_val = train_test_split(
        X_train, y_train, test_size=0.11, stratify=y_train, random_state=42  # 10% of train
    )
    
    # 3. Hyperparameter tuning (5-fold CV)
    param_grid = {
        'n_estimators': [100, 200],
        'max_depth': [5, 6, 7],
        'learning_rate': [0.05, 0.1],
    }
    
    xgb_base = XGBClassifier(
        subsample=0.8,
        colsample_bytree=0.8,
        scale_pos_weight=3,  # Handle class imbalance
        random_state=42
    )
    
    grid_search = GridSearchCV(
        xgb_base, param_grid, cv=5, scoring='f1', n_jobs=-1
    )
    grid_search.fit(X_train, y_train)
    
    best_model = grid_search.best_estimator_
    
    # 4. Train on train + val combined
    X_combined = np.vstack([X_train, X_val])
    y_combined = np.hstack([y_train, y_val])
    best_model.fit(X_combined, y_combined)
    
    # 5. Evaluate on test set
    y_pred = best_model.predict(X_test)
    y_pred_proba = best_model.predict_proba(X_test)[:, 1]
    
    from sklearn.metrics import (
        precision_score, recall_score, f1_score, 
        roc_auc_score, accuracy_score, confusion_matrix
    )
    
    metrics = {
        'accuracy': float(accuracy_score(y_test, y_pred)),
        'precision': float(precision_score(y_test, y_pred)),
        'recall': float(recall_score(y_test, y_pred)),
        'f1': float(f1_score(y_test, y_pred)),
        'roc_auc': float(roc_auc_score(y_test, y_pred_proba)),
        'confusion_matrix': confusion_matrix(y_test, y_pred).tolist(),
    }
    
    # 6. Save model + metrics
    os.makedirs(os.path.dirname(model_path), exist_ok=True)
    joblib.dump(best_model, model_path)
    
    metrics_path = model_path.replace('.pkl', '_metrics.json')
    with open(metrics_path, 'w') as f:
        json.dump(metrics, f, indent=2)
    
    print(f"✓ Model saved to {model_path}")
    print(f"✓ Metrics: Accuracy={metrics['accuracy']:.2%}, Precision={metrics['precision']:.2%}, F1={metrics['f1']:.2%}")
    
    return best_model
```

---

### Model Loading at Startup

```python
# main.py (partial)

import joblib

# Global model variable
ml_model = None

@app.on_event("startup")
async def load_model():
    global ml_model
    try:
        ml_model = joblib.load(settings.MODEL_PATH)
        logger.info(f"✓ ML model loaded from {settings.MODEL_PATH}")
    except FileNotFoundError:
        logger.warning(f"Model not found. Training new model...")
        ml_model = train_model(settings.MODEL_PATH)
        logger.info("✓ Model trained and saved")
```

---

## Services Layer

### matching_service.py

```python
# services/matching_service.py

def check_eligibility(donor: Donor, request: BloodRequest):
    """
    Returns True if donor is eligible for matching with request.
    
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
    
    return (
        donor.available and
        donor.health_eligible and
        18 <= donor.age <= 65 and
        is_compatible(donor.blood_group, request.blood_group_required) and
        days_since >= 90 and
        distance <= 10
    )

def compute_features(donor: Donor, request: BloodRequest, ml_model) -> np.ndarray:
    """
    Compute feature vector for ML prediction (14 features).
    """
    today = date.today()
    distance = haversine_distance(
        donor.latitude, donor.longitude,
        request.latitude, request.longitude
    )
    days_since = (today - donor.last_donation_date).days
    urgency_map = {"LOW": 1, "MEDIUM": 2, "HIGH": 3}
    
    # Donor features
    is_universal = 1 if donor.blood_group == "O-" else 0
    
    # Request features
    urgency_numeric = urgency_map[request.urgency_level]
    
    # Interaction features
    age_compat = abs(donor.age - request.patient_age)
    dist_urgency = distance / urgency_numeric
    recency_urgency = days_since * urgency_numeric
    
    features = np.array([[
        distance, days_since, donor.age, is_universal,
        donor.donation_frequency_6m, donor.successful_previous_matches,
        int(donor.has_adverse_reactions),
        urgency_numeric, request.quantity, request.patient_age, request.request_hour,
        age_compat, dist_urgency, recency_urgency
    ]])
    
    return features

def match_donors(
    session: Session,
    request_id: UUID,
    ml_model
) -> List[DonorMatchResult]:
    """
    Full matching pipeline:
    1. Fetch request
    2. Get all donors
    3. Filter eligible
    4. Compute features + predict
    5. Sort by ml_score descending
    6. Return results
    """
    # 1. Fetch request
    request = session.query(BloodRequest).filter(BloodRequest.id == request_id).first()
    if not request:
        raise ValueError("Request not found")
    
    # 2. Get all donors
    donors = session.query(Donor).all()
    
    # 3-4. Filter + score
    results = []
    for donor in donors:
        if not check_eligibility(donor, request):
            continue
        
        features = compute_features(donor, request, ml_model)
        ml_score = float(ml_model.predict_proba(features)[0, 1])
        distance = haversine_distance(
            donor.latitude, donor.longitude,
            request.latitude, request.longitude
        )
        
        results.append(DonorMatchResult(
            donor_id=donor.id,
            name=donor.name,
            blood_group=donor.blood_group,
            distance_km=round(distance, 2),
            ml_score=round(ml_score, 4)
        ))
    
    # 5. Sort by ml_score descending
    results.sort(key=lambda x: x.ml_score, reverse=True)
    
    # 6. Return (optionally limit to top N)
    return results[:20]  # Top 20 matches
```

---

## API Routes

### GET /match/{request_id}

**Response** (200 OK):
```json
[
  {
    "donor_id": "550e8400-e29b-41d4-a716-446655440000",
    "name": "John Doe",
    "blood_group": "O-",
    "distance_km": 2.3,
    "ml_score": 0.923
  },
  {
    "donor_id": "550e8400-e29b-41d4-a716-446655440001",
    "name": "Jane Smith",
    "blood_group": "O+",
    "distance_km": 5.1,
    "ml_score": 0.876
  }
]
```

### All Endpoints Summary

| Method | Route | Purpose |
|--------|-------|---------|
| POST | `/donors/` | Create donor |
| GET | `/donors/?skip=0&limit=10` | List donors (paginated) |
| GET | `/donors/{id}` | Get single donor |
| PUT | `/donors/{id}` | Update donor |
| POST | `/requests/` | Create request |
| GET | `/requests/?skip=0&limit=10` | List requests (paginated) |
| GET | `/requests/{id}` | Get single request |
| GET | `/match/{request_id}` | Rank matching donors |
| GET | `/health` | Health check |

---

## Implementation Phases

### Phase 1: Environment & Core Setup (2 files)
- [ ] Create `.env` with all variables
- [ ] Create `config.py` with Pydantic BaseSettings

### Phase 2: Database Layer (3 files)
- [ ] `db/database.py` — Engine, SessionLocal, Base
- [ ] `models/donor.py` — Donor ORM model
- [ ] `models/request.py` — BloodRequest ORM model

### Phase 3: Pydantic Schemas (3 files)
- [ ] `schemas/donor.py` — DonorCreate, DonorUpdate, DonorResponse
- [ ] `schemas/request.py` — BloodRequestCreate, BloodRequestResponse
- [ ] `schemas/matching.py` — DonorMatchResult

### Phase 4: Utilities (2 files)
- [ ] `utils/blood_compatibility.py` — is_compatible() + validation
- [ ] `utils/distance.py` — haversine_distance() + threshold check

### Phase 5: ML Module (2 files)
- [ ] `ml/data_generation.py` — generate_synthetic_data()
- [ ] `ml/train.py` — train_model() with XGBoost + metrics

### Phase 6: Services Layer (3 files)
- [ ] `services/donor_service.py` — CRUD + business logic
- [ ] `services/request_service.py` — CRUD
- [ ] `services/matching_service.py` — eligibility + matching

### Phase 7: API Routers (3 files)
- [ ] `routers/donor.py` — POST/GET/PUT endpoints
- [ ] `routers/request.py` — POST/GET endpoints
- [ ] `routers/match.py` — GET /match/{request_id}

### Phase 8: Application Setup (2 files)
- [ ] `app/main.py` — FastAPI init, startup hooks, CORS
- [ ] `requirements.txt` — All dependencies

---

## Verification Checklist

- [ ] PostgreSQL running, database created
- [ ] `.env` file configured correctly
- [ ] `python -m uvicorn app.main:app --reload` starts without errors
- [ ] Model trains on startup and achieves target metrics (Accuracy 90%+, Precision 90%, Recall 85%, F1 0.87)
- [ ] Swagger UI accessible at `http://localhost:8000/docs`
- [ ] POST `/donors/` creates donor, visible in pgAdmin
- [ ] POST `/requests/` creates request
- [ ] GET `/donors/?skip=0&limit=10` returns paginated results
- [ ] GET `/match/{request_id}` returns ranked donors with ml_score
- [ ] Invalid inputs (age > 65, bad blood type) return 422 with `{"detail": "..."}`
- [ ] Missing resources return 404
- [ ] Frontend on `http://localhost:3000` can call endpoints (CORS working)
- [ ] Model file persists at `app/ml/models/model_v1.pkl`
- [ ] Metrics logged to `app/ml/models/model_v1_metrics.json`

---

## Dependencies (requirements.txt)

```
fastapi==0.104.1
uvicorn==0.24.0
sqlalchemy==2.0.23
pydantic==2.5.0
pydantic-settings==2.1.0
psycopg2-binary==2.9.9
xgboost==2.0.0
scikit-learn==1.3.2
joblib==1.3.2
python-multipart==0.0.6
```

---

## Local Run Instructions

```bash
# 1. Activate virtual environment
source venv/bin/activate

# 2. Install dependencies
pip install -r backend/requirements.txt

# 3. Create .env file (see above)

# 4. Ensure PostgreSQL is running and database exists
createdb lifelink

# 5. Start server
python -m uvicorn app.main:app --reload
```

Access Swagger at: **http://localhost:8000/docs**

---

## Notes for Implementation

- **Modular First**: No business logic in routers. All logic in services.
- **Typing**: Use type hints everywhere (Python 3.10+)
- **Error Handling**: Use FastAPI HTTPException with `{"detail": "..."}` format
- **Logging**: Use `logging.getLogger(__name__)` in each module
- **DB Dependencies**: Inject using FastAPI `Depends(get_db)`
- **ML Training**: May take 10-15 seconds on startup. Log progress.
- **Model Persistence**: Always save + metrics for reproducibility

---

**Status**: ✅ READY FOR IMPLEMENTATION

**Questions?** Reference this spec or the session plan at `/memories/session/plan.md`
