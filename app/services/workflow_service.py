from sqlalchemy.orm import Session

from app.repositories.workflow_repository import WorkflowRepository
from app.schemas.workflow import WorkflowCreate


class WorkflowService:
    def __init__(self) -> None:
        self.repository = WorkflowRepository()

    def create_workflow(self, db: Session, workflow_data: WorkflowCreate):
        return self.repository.create_workflow(db, workflow_data)

    def list_workflows(self, db: Session):
        return self.repository.list_workflows(db)

    def get_workflow_by_id(self, db: Session, workflow_id: int):
        return self.repository.get_workflow_by_id(db, workflow_id)