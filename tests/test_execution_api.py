import os
def create_test_workflow(client, step_type="sleep", retry_limit=1):
    payload = {
        "name": "exec-workflow",
        "description": "execution test",
        "steps": [
            {
                "step_order": 1,
                "name": "step1",
                "step_type": step_type,
                "config": {"duration": 1} if step_type == "sleep" else {},
                "retry_limit": retry_limit
            }
        ]
    }
    response = client.post("/workflows", json=payload)
    return response.json()["id"]


def test_execute_workflow_creates_run(client):
    workflow_id = create_test_workflow(client)

    response = client.post(f"/workflows/{workflow_id}/execute")
    assert response.status_code == 200

    data = response.json()
    assert data["workflow_id"] == workflow_id
    assert "id" in data
    assert len(data["task_runs"]) == 1


def test_get_workflow_run(client):
    workflow_id = create_test_workflow(client)

    execute_response = client.post(f"/workflows/{workflow_id}/execute")
    run_id = execute_response.json()["id"]

    response = client.get(f"/workflow-runs/{run_id}")
    assert response.status_code == 200
    assert response.json()["id"] == run_id


def test_get_missing_workflow_run_returns_404(client):
    response = client.get("/workflow-runs/99999")
    assert response.status_code == 404