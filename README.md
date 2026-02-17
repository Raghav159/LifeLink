# LifeLink 🩸

A FastAPI-based blood donation management system that connects blood donors with recipients using intelligent matching algorithms.

## Features

- Donor registration and management
- Blood donation request handling
- AI-powered donor-recipient matching
- Location-based donor discovery
- Health eligibility tracking
- REST API endpoints

## Tech Stack

- **FastAPI** - Web framework
- **PostgreSQL** - Database
- **SQLAlchemy** - ORM
- **Scikit-learn** - Matching algorithms
- **Pytest** - Testing
- **Alembic** - Database migrations

## Quick Start

### Prerequisites

- Python 3.9+
- PostgreSQL

### Setup

1. **Clone & Install**

```bash
git clone <repository-url>
cd LifeLink/backend
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # macOS/Linux
pip install -r requirements.txt
```

2. **Configure Database**
   Create `.env` in `backend/`:

```env
DATABASE_URL=postgresql://username:password@localhost:5432/LifeLink_1
```

⚠️ **Important**: URL-encode special characters in password (e.g., `@` → `%40`)

3. **Create Database & Run**

```bash
createdb LifeLink_1
uvicorn app.main:app --reload
```

API available at: `http://127.0.0.1:8000`

## API Endpoints

| Method | Endpoint             | Description            |
| ------ | -------------------- | ---------------------- |
| GET    | `/`                  | API status             |
| GET    | `/health`            | Health check           |
| POST   | `/donors`            | Register donor         |
| GET    | `/donors/{id}`       | Get donor details      |
| POST   | `/requests`          | Create blood request   |
| GET    | `/requests/{id}`     | Get request details    |
| POST   | `/match/find-donors` | Find compatible donors |

## Project Structure

```
backend/
├── app/
│   ├── main.py           # FastAPI app
│   ├── models/           # Data models (Donor, Request)
│   ├── routers/          # API endpoints
│   ├── db/               # Database setup
│   └── services/         # Business logic
├── tests/                # Unit tests
└── requirements.txt      # Dependencies
```

## Testing

```bash
pytest                    # Run all tests
pytest --cov=app tests/   # With coverage
```

## Interactive API Docs

- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

## Troubleshooting

**Database Connection Error:**
If you see `could not translate host name`, URL-encode special characters in your password:

```env
# Wrong: DATABASE_URL=postgresql://user:pass@word@localhost:5432/db
# Correct:
DATABASE_URL=postgresql://user:pass%40word@localhost:5432/db
```

**Module Not Found:** Run from the `backend/` directory.

## License

MIT License

---

**Connecting donors with those in need** ❤️
