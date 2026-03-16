import time

from sqlalchemy.orm import Session

from app.repositories.execution_repository import ExecutionRepository


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

        workflow_run = self.repository.get_workflow_run_by_id(db, workflow_run.id)
        self.repository.update_workflow_run_status(db, workflow_run, "running")
        db.commit()

        task_runs = self.repository.get_task_runs_for_workflow_run(db, workflow_run.id)

        current_task_run = None

        try:
            for task_run, step in zip(task_runs, sorted_steps):
                current_task_run = task_run

                self.repository.update_task_run_status(
                    db,
                    task_run,
                    "running",
                    started=True,
                )
                db.commit()

                self._execute_step_logic(step.step_type, step.config)

                self.repository.update_task_run_status(
                    db,
                    task_run,
                    "success",
                    completed=True,
                )
                db.commit()

            self.repository.update_workflow_run_status(
                db,
                workflow_run,
                "completed",
                completed=True,
            )
            db.commit()

        except Exception as e:
            if current_task_run:
                self.repository.update_task_run_status(
                    db,
                    current_task_run,
                    "failed",
                    error_message=str(e),
                    completed=True,
                )

            self.repository.update_workflow_run_status(
                db,
                workflow_run,
                "failed",
                completed=True,
            )
            db.commit()

        return self.repository.get_workflow_run_by_id(db, workflow_run.id)

    def get_workflow_run(self, db: Session, run_id: int):
        return self.repository.get_workflow_run_by_id(db, run_id)