import pytest


def get_task_body() -> dict:
    return {
        "title": "Test Task",
        "description": "",
    }


@pytest.mark.asyncio
async def test_successful_task_creation(auth_client):
    res = auth_client.post(
        "/tasks",
        json=get_task_body(),
    )

    assert res.status_code == 200


@pytest.mark.asyncio
async def test_successful_get_list_and_update(auth_client):
    res = auth_client.get(
        "/tasks",
    )

    assert res.status_code == 200
    data = res.json()
    assert isinstance(data, list)
    assert len(data) == 1
    task_to_update = data[0]

    update_data = {**get_task_body(), "description": "Updated description"}
    print("task_to_update", task_to_update)

    res = auth_client.put(
        "/tasks/{}".format(task_to_update["_id"]),
        json=update_data,
    )

    assert res.status_code == 200


@pytest.mark.asyncio
async def test_successful_task_removal(auth_client):
    res = auth_client.get(
        "/tasks",
    )

    assert res.status_code == 200
    data = res.json()
    assert isinstance(data, list)
    assert len(data) == 1
    task_to_delete = data[0]

    res = auth_client.delete(
        "/tasks/{}".format(task_to_delete["_id"]),
    )
    assert res.status_code == 200


@pytest.mark.asyncio
async def test_get_task_not_found(auth_client):
    res = auth_client.put(
        "/tasks/{}".format("689c6829989ea170a9315350"),
        json=get_task_body(),
    )
    assert res.status_code == 404
