from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.base import Base


class TaskRun(Base):
    __tablename__ = "task_runs"

    id = Column(Integer, primary_key=True, index=True)
    workflow_run_id = Column(Integer, ForeignKey("workflow_runs.id", ondelete="CASCADE"), nullable=False)
    workflow_step_id = Column(Integer, ForeignKey("workflow_steps.id", ondelete="CASCADE"), nullable=False)
    status = Column(String(50), nullable=False, default="pending")
    retry_count = Column(Integer, nullable=False, default=0)
    started_at = Column(DateTime(timezone=True), nullable=True)
    completed_at = Column(DateTime(timezone=True), nullable=True)
    error_message = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    workflow_run = relationship("WorkflowRun", back_populates="task_runs")
    workflow_step = relationship("WorkflowStep", back_populates="task_runs")
    logs = relationship("ExecutionLog", back_populates="task_run", cascade="all, delete-orphan")