import uuid
import pytest

from euro_cert_api.schemas.auth import AuthCredentials
from euro_cert_api.schemas.user import CreateUserSchema
from euro_cert_api.common import exceptions


@pytest.mark.asyncio
async def test_successful_user_authenticate(user_manager):
    cred = AuthCredentials(email="josh_test_email@test.com", password="12Qwerty!@")
    user = await user_manager.authenticate(cred)
    assert isinstance(user.id, uuid.UUID)


@pytest.mark.asyncio
async def test_unsuccessful_user_authenticate_wrong_email(user_manager):
    cred = AuthCredentials(email="josh_test_email_222@test.com", password="12Qwerty!@")
    user = await user_manager.authenticate(cred)
    assert user is None


@pytest.mark.asyncio
async def test_unsuccessful_user_creation_bad_password(user_manager):
    with pytest.raises(expected_exception=exceptions.InvalidPasswordException):
        schema = CreateUserSchema(email="josh_test_email123@test.com", password="111")
        await user_manager.create_user(schema)


@pytest.mark.asyncio
async def test_successful_user_creation(user_manager):
    schema = CreateUserSchema(email="josh_test_email123@test.com", password="12345")
    user = await user_manager.create_user(schema)
    assert isinstance(user.id, uuid.UUID)
