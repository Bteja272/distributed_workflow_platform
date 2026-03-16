# Distributed Workflow Automation Platform

A backend platform for defining, managing, and executing multi-step workflows asynchronously. Workflows are composed of discrete, ordered steps that execute sequentially, with full run tracking, status transitions, and error handling at every stage.

---

## Tech Stack

| Layer | Technology |
|---|---|
| API | FastAPI |
| ORM | SQLAlchemy |
| Database | PostgreSQL |
| Task Queue | Celery |
| Broker | Redis |
| Migrations | Alembic |
| Containerization | Docker |

---

## Project Structure
```
app/
├── main.py               # FastAPI app entry point
├── database.py           # DB connection and session management
├── models/               # SQLAlchemy models
│   ├── workflow.py
│   ├── workflow_step.py
│   ├── workflow_run.py
│   ├── task_run.py
│   └── execution_log.py
├── schemas/              # Pydantic request/response schemas
├── repositories/         # Database query layer
├── services/             # Business logic layer
└── routers/              # API route definitions
```

---

## Getting Started

### Prerequisites

- Python 3.10+
- PostgreSQL
- Redis

### Installation

**1. Clone the repo and install dependencies:**
```bash
git clone https://github.com/your-username/your-repo.git
cd your-repo
pip install -r requirements.txt
```

**2. Set up your environment variables:**
```env
DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@localhost:5432/distributed_workflow_db
```

**3. Apply database migrations:**
```bash
alembic upgrade head
```

**4. Start the server:**
```bash
uvicorn app.main:app --reload
```

API docs: http://127.0.0.1:8000/docs

---

## Database Schema

| Table | Description |
|---|---|
| `workflows` | Workflow definitions and metadata |
| `workflow_steps` | Ordered steps belonging to a workflow |
| `workflow_runs` | Individual execution instances of a workflow |
| `task_runs` | Per-step execution records tied to a run |
| `execution_logs` | Timestamped logs and error messages per task |

---

## API Reference

### Workflows

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/workflows` | Create a new workflow |
| `GET` | `/workflows` | List all workflows |
| `GET` | `/workflows/{workflow_id}` | Get a workflow by ID |

### Execution

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/workflows/{workflow_id}/execute` | Trigger a workflow execution |
| `GET` | `/workflow-runs/{run_id}` | Get the status and result of a run |

---

## How Execution Works

When a workflow is executed, the platform creates a `workflow_run` record and initializes a `task_run` for each step with a `pending` status. Steps then run sequentially through the following lifecycle:
```
pending → running → success
                 → failed
```

The overall workflow run resolves as:
- `completed` — all steps succeeded
- `failed` — one or more steps failed

### Supported Step Types

| Type | Description |
|---|---|
| `sleep` | Simulated delay |
| `python` | Simulated internal task |
| `http` | Simulated external API call |
| `fail` | Intentional failure for testing error handling |

---

## Health & Diagnostic Endpoints

| Endpoint | Description |
|---|---|
| `GET /` | Root check |
| `GET /health` | Service health status |
| `GET /db-check` | Verifies live database connectivity |

---

## Environment Variables

| Variable | Description |
|---|---|
| `DATABASE_URL` | PostgreSQL connection string |

---

## Roadmap

- [ ] Async step execution via Celery workers
- [ ] Retry logic for failed steps
- [ ] Webhook notifications on run completion
- [ ] Workflow scheduling (cron-based triggers)
- [ ] Docker Compose setup for full local stack