from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.dependencies import get_db
from app.schemas.workflow import WorkflowCreate, WorkflowResponse
from app.services.workflow_service import WorkflowService

router = APIRouter(prefix="/workflows", tags=["Workflows"])
workflow_service = WorkflowService()


@router.post("", response_model=WorkflowResponse)
def create_workflow(
    workflow_data: WorkflowCreate,
    db: Session = Depends(get_db),
):
    return workflow_service.create_workflow(db, workflow_data)


@router.get("", response_model=list[WorkflowResponse])
def list_workflows(
    db: Session = Depends(get_db),
):
    return workflow_service.list_workflows(db)


@router.get("/{workflow_id}", response_model=WorkflowResponse)
def get_workflow(
    workflow_id: int,
    db: Session = Depends(get_db),
):
    workflow = workflow_service.get_workflow_by_id(db, workflow_id)
    if not workflow:
        raise HTTPException(status_code=404, detail="Workflow not found")
    return workflow