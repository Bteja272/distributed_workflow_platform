from datetime import datetime

from pydantic import BaseModel


class ExecutionLogResponse(BaseModel):
    id: int
    workflow_run_id: int
    task_run_id: int | None = None
    log_level: str
    message: str
    timestamp: datetime

    class Config:
        from_attributes = True