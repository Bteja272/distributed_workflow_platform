from sqlalchemy.orm import Session

from app.repositories.log_repository import LogRepository


class LogService:
    def __init__(self) -> None:
        self.repository = LogRepository()

    def create_log(
        self,
        db: Session,
        workflow_run_id: int,
        log_level: str,
        message: str,
        task_run_id: int | None = None,
    ):
        return self.repository.create_log(
            db=db,
            workflow_run_id=workflow_run_id,
            log_level=log_level,
            message=message,
            task_run_id=task_run_id,
        )

    def get_logs_by_workflow_run_id(self, db: Session, workflow_run_id: int):
        return self.repository.get_logs_by_workflow_run_id(db, workflow_run_id)