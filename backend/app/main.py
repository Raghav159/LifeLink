from fastapi import FastAPI
from app.db.database import Base, engine
from app.models import Donor, BloodRequest
from app.routers import donor, request, match


app = FastAPI(
    title="LifeLink API",
    version="1.0.0"
)

app.include_router(donor.router)
app.include_router(request.router)
app.include_router(match.router)


@app.on_event("startup")
async def startup():
    try:
        # Create tables if they don't exist
        Base.metadata.create_all(bind=engine)
        print("✅ Tables created successfully.")
    except Exception as e:
        print(f"❌ Error creating tables: {e}")


@app.get("/")
async def root():
    return {"message": "LifeLink API is running"}


@app.get("/health")
async def health():
    return {"status": "healthy"}
