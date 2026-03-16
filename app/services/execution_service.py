from sqlalchemy.orm import Session

from app.repositories.execution_repository import ExecutionRepository


class ExecutionService:
    def __init__(self) -> None:
        self.repository = ExecutionRepository()

    def execute_workflow(self, db: Session, workflow_id: int):
        workflow = self.repository.get_workflow_with_steps(db, workflow_id)

        if not workflow:
            return None

        workflow_run = self.repository.create_workflow_run(db, workflow_id)

        sorted_steps = sorted(workflow.steps, key=lambda step: step.step_order)
        self.repository.create_task_runs(db, workflow_run.id, sorted_steps)

        db.commit()

        return self.repository.get_workflow_run_by_id(db, workflow_run.id)

    def get_workflow_run(self, db: Session, run_id: int):
        return self.repository.get_workflow_run_by_id(db, run_id)