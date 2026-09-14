# BidSure AI

AI-assisted, evidence-backed preliminary bid compliance verification platform for SIH26100.

## Architecture

- React + TypeScript frontend
- FastAPI backend
- PostgreSQL
- SQLAlchemy 2.0
- Alembic
- Local file storage
- PostgreSQL-backed processing-job foundation

## Local Setup

### Backend

```powershell
cd backend
uv sync
uv run alembic upgrade head
uv run uvicorn app.main:app --reload