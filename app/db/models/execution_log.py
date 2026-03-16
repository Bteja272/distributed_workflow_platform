from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.base import Base


class ExecutionLog(Base):
    __tablename__ = "execution_logs"

    id = Column(Integer, primary_key=True, index=True)
    workflow_run_id = Column(Integer, ForeignKey("workflow_runs.id", ondelete="CASCADE"), nullable=False)
    task_run_id = Column(Integer, ForeignKey("task_runs.id", ondelete="CASCADE"), nullable=True)
    log_level = Column(String(20), nullable=False, default="INFO")
    message = Column(Text, nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())

    workflow_run = relationship("WorkflowRun", back_populates="logs")
    task_run = relationship("TaskRun", back_populates="logs")