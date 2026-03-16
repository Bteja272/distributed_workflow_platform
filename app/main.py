from fastapi import FastAPI

app = FastAPI(title="Distributed Workflow Automation Platform")


@app.get("/")
def root():
    return {"message": "Distributed Workflow Automation Platform is running"}


@app.get("/health")
def health():
    return {"status": "healthy"}