import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

print("DEBUG DATABASE_URL =", DATABASE_URL)  # 👈 ADD THIS

if not DATABASE_URL:
    raise ValueError("DATABASE_URL is not set in environment variables")

# SQLite doesn't support pool parameters, only PostgreSQL does
engine_kwargs = {
    "pool_pre_ping": True,
}

if "sqlite" not in DATABASE_URL:
    # For PostgreSQL and other databases
    engine_kwargs.update({
        "pool_recycle": 300,
        "pool_size": 5,
        "max_overflow": 10,
    })

engine = create_engine(DATABASE_URL, **engine_kwargs)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()
