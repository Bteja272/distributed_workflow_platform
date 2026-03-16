from sqlalchemy import Column, ForeignKey, Integer, JSON, String
from sqlalchemy.orm import relationship

from app.db.base import Base


class WorkflowStep(Base):
    __tablename__ = "workflow_steps"

    id = Column(Integer, primary_key=True, index=True)
    workflow_id = Column(Integer, ForeignKey("workflows.id", ondelete="CASCADE"), nullable=False)
    step_order = Column(Integer, nullable=False)
    name = Column(String(255), nullable=False)
    step_type = Column(String(100), nullable=False)
    config = Column(JSON, nullable=True)
    retry_limit = Column(Integer, nullable=False, default=3)

    workflow = relationship("Workflow", back_populates="steps")
    task_runs = relationship("TaskRun", back_populates="workflow_step")