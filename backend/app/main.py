import logging
import joblib
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.db.database import Base, engine
from app.models import Donor, BloodRequest
from app.routers import donor, request, match
from app.core.config import settings, logger
from app.ml.train import train_model

# Global ML model variable
ml_model = None

app = FastAPI(
    title="LifeLink API",
    version="1.0.0",
    description="Blood donor matching platform with ML-powered ranking"
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
        "http://localhost:8000",
        settings.FRONTEND_URL,
        "*"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    allow_origin_regex=".*",
)

app.include_router(donor.router)
app.include_router(request.router)
app.include_router(match.router)


@app.on_event("startup")
async def startup():
    """Initialize database and load ML model on startup"""
    global ml_model
    
    logger.info("🚀 Starting LifeLink backend...")
    
    # Create tables (do NOT drop existing data)
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("✅ Database tables created/verified")
    except Exception as e:
        logger.error(f"❌ Error creating tables: {e}")
        raise
    
    # Load or train ML model
    try:
        logger.info(f"Loading ML model from {settings.MODEL_PATH}...")
        ml_model = joblib.load(settings.MODEL_PATH)
        logger.info("✅ ML model loaded successfully")
    except FileNotFoundError:
        logger.warning(f"Model not found at {settings.MODEL_PATH}. Training new model...")
        try:
            ml_model = train_model(settings.MODEL_PATH)
            logger.info("✅ ML model trained and saved")
        except Exception as e:
            logger.error(f"❌ Error training model: {e}")
            raise


@app.get("/")
async def root():
    return {
        "message": "LifeLink API is running",
        "docs": "/docs",
        "redoc": "/redoc"
    }


@app.get("/health")
async def health():
    return {"status": "healthy", "database": "connected"}
