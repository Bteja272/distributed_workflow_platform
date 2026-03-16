from fastapi import FastAPI
from sqlalchemy import text

from app.api.routes.workflows import router as workflow_router
from app.db.base import Base
from app.db.session import engine
from app.db import models  # noqa: F401

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Distributed Workflow Automation Platform")

app.include_router(workflow_router)


@app.get("/")
def root():
    return {"message": "Distributed Workflow Automation Platform is running"}


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.get("/db-check")
def db_check():
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        return {"database": "connected"}
    except Exception as e:
        return {"database": "failed", "error": str(e)}


@app.get("/tables-check")
def tables_check():
    try:
        with engine.connect() as connection:
            result = connection.execute(text("""
                SELECT table_name
                FROM information_schema.tables
                WHERE table_schema = 'public'
                ORDER BY table_name
            """))
            tables = [row[0] for row in result]
        return {"tables": tables}
    except Exception as e:
        return {"error": str(e)}