import time

from app.core.celery_app import celery_app
from app.db.session import SessionLocal
from app.repositories.execution_repository import ExecutionRepository


@celery_app.task
def execute_workflow_task(workflow_run_id: int):
    db = SessionLocal()
    repository = ExecutionRepository()

    workflow_run = repository.get_workflow_run_by_id(db, workflow_run_id)

    if not workflow_run:
        return

    repository.update_workflow_run_status(db, workflow_run, "running")
    db.commit()

    task_runs = repository.get_task_runs_for_workflow_run(db, workflow_run_id)

    current_task_run = None

    try:
        for task_run in task_runs:
            current_task_run = task_run

            repository.update_task_run_status(
                db, task_run, "running", started=True
            )
            db.commit()

            # simulate execution
            step_type = task_run.workflow_step.step_type

            if step_type == "sleep":
                time.sleep(2)
            elif step_type == "fail":
                raise Exception("Simulated failure")
            else:
                time.sleep(1)

            repository.update_task_run_status(
                db, task_run, "success", completed=True
            )
            db.commit()

        repository.update_workflow_run_status(
            db, workflow_run, "completed", completed=True
        )
        db.commit()

    except Exception as e:
        if current_task_run:
            repository.update_task_run_status(
                db,
                current_task_run,
                "failed",
                error_message=str(e),
                completed=True,
            )

        repository.update_workflow_run_status(
            db, workflow_run, "failed", completed=True
        )
        db.commit()

    finally:
        db.close()