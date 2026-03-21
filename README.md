# Distributed Workflow Automation Platform

A backend system for defining and executing multi-step workflows asynchronously,
with built-in retry logic, failure handling, and execution logging.

Inspired by workflow orchestration tools like Apache Airflow and Temporal.

---

## Tech Stack

| Layer | Technology |
|---|---|
| API | FastAPI (Python 3.11) |
| Database | PostgreSQL + SQLAlchemy |
| Task Queue | Celery |
| Message Broker | Redis |
| Containerization | Docker & Docker Compose |

---

## Features

- Create and manage multi-step workflows via REST API
- Asynchronous background execution using Celery workers
- Configurable per-step retry logic with attempt tracking
- Sequential step execution with status transitions
- Persistent execution logs queryable through the API
- Fully containerized — runs with a single Docker command

---

## Project Structure
```
app/
├── api/
│   └── routes/
├── core/
│   ├── config.py
│   └── celery_app.py
├── db/
│   ├── models/
│   ├── session.py
│   └── base.py
├── repositories/
├── services/
├── workers/
│   └── tasks.py
└── schemas/
```

---

## Getting Started

### Docker (Recommended)

Run the full stack with a single command:
```bash
docker compose up --build
```

API docs: http://127.0.0.1:8000/docs
```bash
docker compose down  # Stop all services
```

---

### Local Development

**1. Create and activate a virtual environment:**
```bash
python -m venv .venv
.venv\Scripts\activate      # Windows
source .venv/bin/activate   # macOS/Linux
```

**2. Install dependencies:**
```bash
pip install -r requirements.txt
```

**3. Configure environment variables:**
```env
DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@localhost:5432/distributed_workflow_db
REDIS_URL=redis://localhost:6379/0
```

**4. Start FastAPI:**
```bash
uvicorn app.main:app --reload
```

**5. Start Celery worker:**
```bash
celery -A app.core.celery_app worker --pool=solo --loglevel=info
```

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
| `POST` | `/workflows/{workflow_id}/execute` | Trigger workflow execution |
| `GET` | `/workflow-runs/{run_id}` | Get run status |
| `GET` | `/workflow-runs/{run_id}/logs` | Get execution logs |

---

## Example Workflow
```json
{
  "name": "sample-workflow",
  "description": "Example workflow",
  "steps": [
    {
      "step_order": 1,
      "name": "step_one",
      "step_type": "sleep",
      "config": { "duration": 1 },
      "retry_limit": 1
    },
    {
      "step_order": 2,
      "name": "step_two",
      "step_type": "fail",
      "config": {},
      "retry_limit": 2
    }
  ]
}
```

---

## Execution Flow

1. Workflow is created via the API
2. An execution request dispatches a Celery task
3. The worker processes each step sequentially:
   - Status updated in the database (`pending → running → success / failed`)
   - Execution events written to logs
   - Failed steps are retried up to the configured `retry_limit`
4. Final workflow status (`completed` or `failed`) is persisted

---

## Roadmap

- [ ] Parallel step execution
- [ ] DAG-based workflow definitions
- [ ] Monitoring dashboard (Grafana / Prometheus)
- [ ] Authentication and multi-user support
- [ ] Workflow visualization UI