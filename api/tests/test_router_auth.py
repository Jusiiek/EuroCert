import pytest


@pytest.mark.asyncio
async def test_successful_login(test_client):
    res = test_client.post(
        "/auth/login",
        json={
            "email": "josh_test_email@test.com",
            "password": "J0$h123456"
        }
    )
    assert res.status_code == 200
    data = res.json()

    assert "token_type" in data.keys()
    assert "access_token" in data.keys()


@pytest.mark.asyncio
async def test_unsuccessful_login_user_inactive(test_client):
    res = test_client.post(
        "/auth/login",
        json={
            "email": "inactive_user@test.com",
            "password": "3L&sabeth123456"
        }
    )
    assert res.status_code == 400


@pytest.mark.asyncio
async def test_unsuccessful_login_user_does_not_exists(test_client):
    res = test_client.post(
        "/auth/login",
        json={
            "email": "inactive_user_2@test.com",
            "password": "3L&sabeth123456"
        }
    )
    assert res.status_code == 400


@pytest.mark.asyncio
async def test_successful_register(test_client):
    res = test_client.post(
        "/auth/register",
        json={
            "email": "inactive_user_2@test.com",
            "password": "J0$h123456"
        }
    )
    assert res.status_code == 200


@pytest.mark.asyncio
async def test_unsuccessful_register_wrong_password(test_client):
    res = test_client.post(
        "/auth/register",
        json={
            "email": "inactive_user_3@test.com",
            "password": "12345"
        }
    )
    assert res.status_code == 400


@pytest.mark.asyncio
async def test_unsuccessful_register_user_already_exists(test_client):
    res = test_client.post(
        "/auth/register",
        json={
            "email": "inactive_user_2@test.com",
            "password": "J0$h123456"
        }
    )
    assert res.status_code == 400
