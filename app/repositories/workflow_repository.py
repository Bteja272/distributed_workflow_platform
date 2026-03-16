from sqlalchemy.orm import Session, joinedload

from app.db.models.workflow import Workflow
from app.db.models.workflow_step import WorkflowStep
from app.schemas.workflow import WorkflowCreate


class WorkflowRepository:
    def create_workflow(self, db: Session, workflow_data: WorkflowCreate) -> Workflow:
        workflow = Workflow(
            name=workflow_data.name,
            description=workflow_data.description,
        )
        db.add(workflow)
        db.flush()

        for step in workflow_data.steps:
            workflow_step = WorkflowStep(
                workflow_id=workflow.id,
                step_order=step.step_order,
                name=step.name,
                step_type=step.step_type,
                config=step.config,
                retry_limit=step.retry_limit,
            )
            db.add(workflow_step)

        db.commit()
        db.refresh(workflow)

        workflow_with_steps = (
            db.query(Workflow)
            .options(joinedload(Workflow.steps))
            .filter(Workflow.id == workflow.id)
            .first()
        )
        return workflow_with_steps

    def list_workflows(self, db: Session) -> list[Workflow]:
        return (
            db.query(Workflow)
            .options(joinedload(Workflow.steps))
            .order_by(Workflow.id)
            .all()
        )

    def get_workflow_by_id(self, db: Session, workflow_id: int) -> Workflow | None:
        return (
            db.query(Workflow)
            .options(joinedload(Workflow.steps))
            .filter(Workflow.id == workflow_id)
            .first()
        )