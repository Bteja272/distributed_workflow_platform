from sqlalchemy.orm import Session

from app.db.models.execution_log import ExecutionLog


class LogRepository:
    def create_log(
        self,
        db: Session,
        workflow_run_id: int,
        log_level: str,
        message: str,
        task_run_id: int | None = None,
    ) -> ExecutionLog:
        log = ExecutionLog(
            workflow_run_id=workflow_run_id,
            task_run_id=task_run_id,
            log_level=log_level,
            message=message,
        )
        db.add(log)
        return log

    def get_logs_by_workflow_run_id(self, db: Session, workflow_run_id: int) -> list[ExecutionLog]:
        return (
            db.query(ExecutionLog)
            .filter(ExecutionLog.workflow_run_id == workflow_run_id)
            .order_by(ExecutionLog.timestamp, ExecutionLog.id)
            .all()
        )