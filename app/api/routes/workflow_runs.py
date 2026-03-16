from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.dependencies import get_db
from app.schemas.workflow_run import WorkflowRunResponse
from app.services.execution_service import ExecutionService

router = APIRouter(tags=["Workflow Runs"])
execution_service = ExecutionService()


@router.post("/workflows/{workflow_id}/execute", response_model=WorkflowRunResponse)
def execute_workflow(
    workflow_id: int,
    db: Session = Depends(get_db),
):
    workflow_run = execution_service.execute_workflow(db, workflow_id)
    if not workflow_run:
        raise HTTPException(status_code=404, detail="Workflow not found")
    return workflow_run


@router.get("/workflow-runs/{run_id}", response_model=WorkflowRunResponse)
def get_workflow_run(
    run_id: int,
    db: Session = Depends(get_db),
):
    workflow_run = execution_service.get_workflow_run(db, run_id)
    if not workflow_run:
        raise HTTPException(status_code=404, detail="Workflow run not found")
    return workflow_run