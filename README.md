# Distributed Workflow Automation Platform

A backend system that allows users to create and execute multi-step workflows asynchronously.

## Tech Stack

- Python
- FastAPI
- Redis
- Celery
- PostgreSQL
- Docker

---

## Day 1 Progress

- Project repository initialized
- Python virtual environment created
- FastAPI application created
- Basic API endpoints added

**Run the FastAPI server:**
```bash
uvicorn app.main:app --reload
```

**Test endpoints:**
- http://127.0.0.1:8000/
- http://127.0.0.1:8000/health
- http://127.0.0.1:8000/docs

---

## Day 2 Progress

- PostgreSQL installed and configured
- Project database created (`distributed_workflow_db`)
- Environment variables configured using `.env`
- Database dependencies installed (`SQLAlchemy`, `psycopg2-binary`, `python-dotenv`, `alembic`)
- Database connection module implemented
- SQLAlchemy base model created
- FastAPI database connectivity test endpoint added

**Install database dependencies:**
```bash
pip install sqlalchemy psycopg2-binary python-dotenv alembic
```

**Update project dependencies:**
```bash
pip freeze > requirements.txt
```

**Create `.env` configuration:**
```env
DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@localhost:5432/distributed_workflow_db
```

**Run the FastAPI server:**
```bash
uvicorn app.main:app --reload
```

**Verify database connection:**
- http://127.0.0.1:8000/db-check

**Expected response:**
```json
{"database": "connected"}
```