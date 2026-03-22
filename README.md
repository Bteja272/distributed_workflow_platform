# Distributed Workflow Automation Platform

A backend system for defining and executing multi-step workflows asynchronously,
with retry handling, execution logging, and real external HTTP integrations.

Inspired by workflow orchestration tools like Apache Airflow and Temporal.

---

## Tech Stack

| Layer | Technology |
|---|---|
| API | FastAPI (Python 3.11) |
| Database | PostgreSQL + SQLAlchemy |
| Task Queue | Celery |
| Message Broker | Redis |
| Testing | Pytest |
| Containerization | Docker & Docker Compose |

---

## Features

- Create and manage multi-step workflows via REST API
- Asynchronous background execution using Celery workers
- Configurable per-step retry logic with attempt tracking
- Sequential step execution with full status lifecycle management
- Real external HTTP integrations with failure and retry handling
- Persistent execution logs queryable through the API
- Isolated test suite using SQLite and mocked Celery tasks
- Fully containerized — runs with a single Docker command

---

## System Architecture
```
Client → FastAPI → PostgreSQL
              ↓
     Celery Worker ← Redis (Broker)
```

- **FastAPI** — handles all incoming API requests
- **PostgreSQL** — stores workflows, runs, task states, and logs
- **Redis** — message broker between FastAPI and Celery
- **Celery Worker** — executes workflow steps asynchronously in the background

---

## Project Structure
```
app/
├── api/              # FastAPI route definitions
├── core/             # Config and Celery setup
├── db/               # Models, session, and base
├── repositories/     # Database access layer
├── services/         # Business logic
├── workers/          # Celery task execution
└── schemas/          # Pydantic request/response schemas

tests/
├── conftest.py
├── test_workflows_api.py
└── test_execution_api.py
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

**4. Start the API:**
```bash
uvicorn app.main:app --reload
```

**5. Start the Celery worker:**
```bash
celery -A app.core.celery_app worker --pool=solo --loglevel=info
```

---

## Running Tests
```bash
pytest
```

**Testing notes:**
- Uses an isolated SQLite database — no PostgreSQL required
- Celery tasks are mocked — no Redis required
- Coverage includes workflow creation, execution flow, run retrieval, and error handling

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

This example demonstrates a real external HTTP call followed by a processing step:
```json
{
  "name": "real-http-workflow",
  "description": "Fetch data from an external API",
  "steps": [
    {
      "step_order": 1,
      "name": "fetch_joke",
      "step_type": "http",
      "config": {
        "url": "https://official-joke-api.appspot.com/random_joke",
        "method": "GET",
        "timeout": 10
      },
      "retry_limit": 2
    },
    {
      "step_order": 2,
      "name": "post_process",
      "step_type": "python",
      "config": {},
      "retry_limit": 1
    }
  ]
}
```

---

## Execution Flow

1. Workflow is created via the API
2. An execution request dispatches a Celery task to Redis
3. The worker picks up the task and processes each step sequentially:
   - Step status updated in the database (`pending → running → success / failed`)
   - Execution events written to logs
   - Failed steps are retried up to the configured `retry_limit`
4. Final workflow status resolves to `completed` or `failed` and is persisted

---

## Roadmap

- [ ] Parallel step execution
- [ ] DAG-based workflow definitions
- [ ] Monitoring dashboard (Grafana / Prometheus)
- [ ] Authentication and multi-user support
- [ ] Workflow visualization UI