def test_create_workflow(client):
    payload = {
        "name": "test-workflow",
        "description": "test",
        "steps": [
            {
                "step_order": 1,
                "name": "step1",
                "step_type": "sleep",
                "config": {"duration": 1},
                "retry_limit": 1
            }
        ]
    }

    response = client.post("/workflows", json=payload)
    assert response.status_code == 200

    data = response.json()
    assert data["name"] == "test-workflow"
    assert len(data["steps"]) == 1
    assert data["steps"][0]["name"] == "step1"


def test_list_workflows(client):
    response = client.get("/workflows")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_workflow_by_id(client):
    payload = {
        "name": "lookup-workflow",
        "description": "lookup",
        "steps": [
            {
                "step_order": 1,
                "name": "step1",
                "step_type": "sleep",
                "config": {"duration": 1},
                "retry_limit": 1
            }
        ]
    }

    create_response = client.post("/workflows", json=payload)
    workflow_id = create_response.json()["id"]

    response = client.get(f"/workflows/{workflow_id}")
    assert response.status_code == 200
    assert response.json()["id"] == workflow_id


def test_get_missing_workflow_returns_404(client):
    response = client.get("/workflows/99999")
    assert response.status_code == 404