from datetime import datetime

from pydantic import BaseModel


class TaskRunResponse(BaseModel):
    id: int
    workflow_step_id: int
    status: str
    retry_count: int
    started_at: datetime | None = None
    completed_at: datetime | None = None
    error_message: str | None = None

    class Config:
        from_attributes = True


class WorkflowRunResponse(BaseModel):
    id: int
    workflow_id: int
    status: str
    started_at: datetime | None = None
    completed_at: datetime | None = None
    task_runs: list[TaskRunResponse]

    class Config:
        from_attributes = True