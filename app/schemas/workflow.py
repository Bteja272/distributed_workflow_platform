from typing import Any

from pydantic import BaseModel, Field


class WorkflowStepCreate(BaseModel):
    step_order: int = Field(..., gt=0)
    name: str
    step_type: str
    config: dict[str, Any] | None = None
    retry_limit: int = Field(default=3, ge=0)


class WorkflowCreate(BaseModel):
    name: str
    description: str | None = None
    steps: list[WorkflowStepCreate]


class WorkflowStepResponse(BaseModel):
    id: int
    step_order: int
    name: str
    step_type: str
    config: dict[str, Any] | None = None
    retry_limit: int

    class Config:
        from_attributes = True


class WorkflowResponse(BaseModel):
    id: int
    name: str
    description: str | None = None
    steps: list[WorkflowStepResponse]

    class Config:
        from_attributes = True