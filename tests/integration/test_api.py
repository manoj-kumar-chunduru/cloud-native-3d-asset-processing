from fastapi.testclient import TestClient

from asset_platform.api import app

client = TestClient(app)


def test_health():
    assert client.get("/health").json() == {"status": "ok"}


def test_register_and_process_asset():
    response = client.post(
        "/assets",
        json={
            "name": "scene.glb",
            "content": "demo-scene",
            "format": "glb",
        },
    )
    assert response.status_code == 201
    asset_id = response.json()["asset_id"]

    job_response = client.post(f"/assets/{asset_id}/process")
    assert job_response.status_code == 200
    assert job_response.json()["asset_id"] == asset_id
