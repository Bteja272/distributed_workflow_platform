from sqlalchemy.orm import Session, joinedload

from app.db.models.task_run import TaskRun
from app.db.models.workflow import Workflow
from app.db.models.workflow_run import WorkflowRun


class ExecutionRepository:
    def get_workflow_with_steps(self, db: Session, workflow_id: int) -> Workflow | None:
        return (
            db.query(Workflow)
            .options(joinedload(Workflow.steps))
            .filter(Workflow.id == workflow_id)
            .first()
        )

    def create_workflow_run(self, db: Session, workflow_id: int) -> WorkflowRun:
        workflow_run = WorkflowRun(
            workflow_id=workflow_id,
            status="pending",
        )
        db.add(workflow_run)
        db.flush()
        return workflow_run

    def create_task_runs(self, db: Session, workflow_run_id: int, steps: list) -> None:
        for step in steps:
            task_run = TaskRun(
                workflow_run_id=workflow_run_id,
                workflow_step_id=step.id,
                status="pending",
                retry_count=0,
            )
            db.add(task_run)

    def get_workflow_run_by_id(self, db: Session, run_id: int) -> WorkflowRun | None:
        return (
            db.query(WorkflowRun)
            .options(joinedload(WorkflowRun.task_runs))
            .filter(WorkflowRun.id == run_id)
            .first()
        )