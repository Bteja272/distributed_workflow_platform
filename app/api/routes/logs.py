from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.dependencies import get_db
from app.schemas.log import ExecutionLogResponse
from app.services.log_service import LogService

router = APIRouter(tags=["Logs"])
log_service = LogService()


@router.get("/workflow-runs/{run_id}/logs", response_model=list[ExecutionLogResponse])
def get_workflow_run_logs(
    run_id: int,
    db: Session = Depends(get_db),
):
    return log_service.get_logs_by_workflow_run_id(db, run_id)