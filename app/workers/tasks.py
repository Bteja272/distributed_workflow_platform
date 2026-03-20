import time

from app.core.celery_app import celery_app
from app.db.session import SessionLocal
from app.repositories.execution_repository import ExecutionRepository


@celery_app.task
def execute_workflow_task(workflow_run_id: int):
    db = SessionLocal()
    repository = ExecutionRepository()

    try:
        workflow_run = repository.get_workflow_run_by_id(db, workflow_run_id)

        if not workflow_run:
            return

        repository.update_workflow_run_status(db, workflow_run, "running")
        db.commit()

        task_runs = repository.get_task_runs_for_workflow_run(db, workflow_run_id)

        for task_run in task_runs:
            step = task_run.workflow_step
            retry_limit = step.retry_limit

            repository.update_task_run_status(
                db,
                task_run,
                "running",
                started=True,
                error_message=None,
            )
            db.commit()

            success = False

            for attempt in range(retry_limit + 1):
                try:
                    step_type = step.step_type

                    if step_type == "sleep":
                        duration = 2
                        if step.config and "duration" in step.config:
                            duration = int(step.config["duration"])
                        time.sleep(duration)

                    elif step_type == "fail":
                        raise Exception("Simulated task failure")

                    elif step_type == "http":
                        time.sleep(1)

                    elif step_type == "python":
                        time.sleep(1)

                    else:
                        time.sleep(1)

                    repository.update_task_run_status(
                        db,
                        task_run,
                        "success",
                        completed=True,
                        error_message=None,
                    )
                    db.commit()

                    success = True
                    break

                except Exception as e:
                    if attempt < retry_limit:
                        repository.increment_task_retry_count(db, task_run)
                        repository.update_task_run_status(
                            db,
                            task_run,
                            "retrying",
                            error_message=str(e),
                        )
                        db.commit()

                        time.sleep(2)
                    else:
                        repository.update_task_run_status(
                            db,
                            task_run,
                            "failed",
                            error_message=str(e),
                            completed=True,
                        )
                        db.commit()

                        raise

            if not success:
                raise Exception(f"Workflow failed because task_run={task_run.id} failed after retries")

        repository.update_workflow_run_status(
            db,
            workflow_run,
            "completed",
            completed=True,
        )
        db.commit()

    except Exception:
        workflow_run = repository.get_workflow_run_by_id(db, workflow_run_id)
        if workflow_run:
            repository.update_workflow_run_status(
                db,
                workflow_run,
                "failed",
                completed=True,
            )
            db.commit()

    finally:
        db.close()