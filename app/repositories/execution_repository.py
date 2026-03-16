from datetime import datetime

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

    def update_workflow_run_status(
        self,
        db: Session,
        workflow_run: WorkflowRun,
        status: str,
        completed: bool = False,
    ) -> None:
        workflow_run.status = status
        if completed:
            workflow_run.completed_at = datetime.utcnow()
        db.add(workflow_run)

    def update_task_run_status(
        self,
        db: Session,
        task_run: TaskRun,
        status: str,
        error_message: str | None = None,
        started: bool = False,
        completed: bool = False,
    ) -> None:
        task_run.status = status
        if started:
            task_run.started_at = datetime.utcnow()
        if completed:
            task_run.completed_at = datetime.utcnow()
        if error_message:
            task_run.error_message = error_message
        db.add(task_run)

    def get_task_runs_for_workflow_run(self, db: Session, workflow_run_id: int) -> list[TaskRun]:
        return (
            db.query(TaskRun)
            .filter(TaskRun.workflow_run_id == workflow_run_id)
            .order_by(TaskRun.id)
            .all()
        )