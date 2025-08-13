import uuid
import asyncio
import dataclasses
from typing import Optional, List, Any

import pytest
from pydantic import UUID4
from fastapi.security.base import SecurityBase
from fastapi import Request
from fastapi.testclient import TestClient

from euro_cert_api.managers.user import UserManager
from euro_cert_api.authtentication.authenticator import Authenticator
from euro_cert_api.authtentication.transport import Transport
from euro_cert_api.authtentication.backend import AuthenticationBackend
from euro_cert_api.authtentication.strategy.jwt import JWTStrategy
from euro_cert_api.models.user import User
from euro_cert_api.utils.password import PasswordHelper
from euro_cert_api.schemas.user import CreateUserSchema
from euro_cert_api.schemas.auth import AuthCredentials
from euro_cert_api.common import exceptions
from euro_cert_api.app import app


loop = asyncio.get_event_loop()
client = TestClient(app)


IDType = UUID4

password_helper = PasswordHelper()
josh_password_hash = password_helper.hash_password('12Qwerty!@')
elisabeth_password_hash = password_helper.hash_password('elisabeth')


@dataclasses.dataclass
class UserModel:
    email: str
    hashed_password: str
    id: IDType = dataclasses.field(default_factory=uuid.uuid4)
    is_active: bool = True


class MockSecurityScheme(SecurityBase):
    def __call__(self, request: Request) -> Optional[str]:
        return "mock"


class MockTransport(Transport):
    def __init__(self):
        super().__init__("mock")
        self.scheme = MockSecurityScheme()


class MockStrategy(JWTStrategy):

    async def read_token(self, token: Optional[str], user_manager: UserManager) -> Optional[User]:
        if token is not None:
            try:
                parsed_id = user_manager.parse_id(token)
                return await user_manager.get_by_id(parsed_id)
            except Exception as e:
                return None
        return None

    async def write_token(self, user: UserModel):
        return str(user.id)

    async def destroy_token(self, token: str) -> None:
        return None


class MockUserManager(UserManager):

    def __init__(self, password_helper: PasswordHelper = None):
        super().__init__(password_helper)
        self._users: List[UserModel] = [
            UserModel(
                email='josh_test_email@test.com',
                hashed_password=josh_password_hash,
                id=uuid.UUID("5b7827a7-6c8d-4b7a-926d-0b2ac7af7d7e")
            ),
            UserModel(
                email='elisabeth_test_email@test.com',
                hashed_password=elisabeth_password_hash,
                id=uuid.UUID("0cc735ff-39f8-4b63-b08e-c50a9adbf709"),
                is_active=False
            )
        ]

    def parse_id(self, id: Any) -> IDType:
        return str(id)

    async def get_by_id(self, id: str) -> Optional[UserModel]:
        user = [u for u in self._users if str(u.id) == id][0] or None
        if user is None:
            raise exceptions.UserNotExists()
        return user

    async def get_by_email(self, email: str) -> Optional[UserModel]:
        user = [u for u in self._users if u.email == email]
        user = user[0] if len(user) > 0 else None
        if user is None:
            raise exceptions.UserNotExists()
        return user

    async def _validate_password(self, password: str) -> None:
        if len(password) < 4:
            raise exceptions.InvalidPasswordException(
                "Password must be at least 4 characters long."
            )

    async def create_user(self, user_create: CreateUserSchema) -> UserModel:
        await self._validate_password(user_create.password)

        try:
            await self.get_by_email(user_create.email)
            raise exceptions.UserAlreadyExists()
        except exceptions.UserNotExists:
            pass

        created_user = UserModel(
            email=user_create.email,
            hashed_password=self.password_helper.hash_password(user_create.password),
            )
        self._users.append(created_user)
        return created_user

    async def authenticate(
            self,
            credentials: AuthCredentials
    ) -> Optional[UserModel]:
        try:
            user: UserModel = await self.get_by_email(credentials.email)
        except exceptions.UserNotExists:
            return None

        verified = self.password_helper.verify_password(
            credentials.password, user.hashed_password
        )
        if not verified:
            return None

        return user


@pytest.fixture
def strategy() -> JWTStrategy:
    return MockStrategy(
        "secret",
        60*60*24
    )


@pytest.fixture
def transport() -> Transport:
    return MockTransport()


@pytest.fixture
def user_manager() -> UserManager:
    return MockUserManager()


@pytest.fixture
def authenticator(user_manager, strategy) -> Authenticator:
    return Authenticator(user_manager, strategy)


@pytest.fixture
def authentication_backend(transport, strategy) -> AuthenticationBackend:
    return AuthenticationBackend(transport, strategy)


@pytest.fixture
def user() -> UserModel:
    return UserModel(
        email='josh_test_email@test.com',
        hashed_password=josh_password_hash,
        id=uuid.UUID("5b7827a7-6c8d-4b7a-926d-0b2ac7af7d7e")
    )


@pytest.fixture
def inactive_user() -> UserModel:
    return UserModel(
        email='elisabeth_test_email@test.com',
        hashed_password=elisabeth_password_hash,
        id=uuid.UUID("0cc735ff-39f8-4b63-b08e-c50a9adbf709"),
        is_active=False
    )


def get_token(
        client: TestClient,
        email: str="josh_test_email@test.com",
        password: str = "J0$h123456"
):
    res = client.post("/auth/login", json={"email": email, "password": password})
    assert res.status_code == 200
    data = res.json()
    return f"{data['token_type']} {data['access_token']}"


@pytest.fixture
def test_client():
    """
    It's necessary to make router test works, due to beanie initialization error.
    """
    with TestClient(app) as client:
        yield client


@pytest.fixture
def auth_client():
    with TestClient(app) as client:
        client.headers.update({"Authorization": get_token(client)})
        yield client
