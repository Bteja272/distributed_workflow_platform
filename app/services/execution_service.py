import time

from sqlalchemy.orm import Session

from app.repositories.execution_repository import ExecutionRepository
from app.workers.tasks import execute_workflow_task


class ExecutionService:
    def __init__(self) -> None:
        self.repository = ExecutionRepository()

    def _execute_step_logic(self, step_type: str, config: dict | None) -> None:
        if step_type == "http":
            time.sleep(1)
        elif step_type == "python":
            time.sleep(1)
        elif step_type == "sleep":
            duration = 2
            if config and "duration" in config:
                duration = int(config["duration"])
            time.sleep(duration)
        elif step_type == "fail":
            raise Exception("Simulated task failure")
        else:
            time.sleep(1)
    def execute_workflow(self, db: Session, workflow_id: int):
        workflow = self.repository.get_workflow_with_steps(db, workflow_id)
        if not workflow:
            return None

        workflow_run = self.repository.create_workflow_run(db, workflow_id)

        sorted_steps = sorted(workflow.steps, key=lambda step: step.step_order)
        self.repository.create_task_runs(db, workflow_run.id, sorted_steps)

        db.commit()

        # Send job to Celery instead of executing here
        execute_workflow_task.delay(workflow_run.id)

        return self.repository.get_workflow_run_by_id(db, workflow_run.id)

    def get_workflow_run(self, db: Session, run_id: int):
        return self.repository.get_workflow_run_by_id(db, run_id)