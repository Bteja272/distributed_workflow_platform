from fastapi import FastAPI
from sqlalchemy import text
from app.db.session import engine

app = FastAPI(title="Distributed Workflow Automation Platform")


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