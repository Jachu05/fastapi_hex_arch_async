import pytest
from httpx import AsyncClient

from app.main import get_application


@pytest.fixture()
def anyio_backend():
    return "asyncio"


@pytest.fixture()
def app():
    # Arrange
    return get_application()


@pytest.fixture()
async def client(app):
    async with AsyncClient(app=app, base_url="http://testserver") as ac:
        yield ac


@pytest.mark.anyio
async def test_create_and_list_task(client):
    # Arrange
    payload = {"description": "Write unit tests"}

    # Act
    create_res = await client.post("/tasks/", json=payload)
    list_res = await client.get("/tasks/")

    # Assert
    assert create_res.status_code == 201
    created = create_res.json()
    assert created["id"] == 1
    assert created["description"] == payload["description"]

    assert list_res.status_code == 200
    tasks = list_res.json()
    assert len(tasks) == 1
    assert tasks[0]["description"] == payload["description"]


@pytest.mark.anyio
async def test_delete_task(client):
    # Arrange
    payload = {"description": "Temp task"}
    create_res = await client.post("/tasks/", json=payload)
    task_id = create_res.json()["id"]

    # Act
    del_res = await client.delete(f"/tasks/{task_id}")
    get_res = await client.get(f"/tasks/{task_id}")

    # Assert
    assert del_res.status_code == 204
    assert get_res.status_code == 404 
