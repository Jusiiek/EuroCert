import uuid
import dataclasses
from typing import Optional

import pytest
from pydantic import UUID4

from euro_cert_api.managers.user import UserManager
from euro_cert_api.authtentication.authenticator import Authenticator
from euro_cert_api.authtentication.transport import Transport
from euro_cert_api.authtentication.backend import AuthenticationBackend
from euro_cert_api.authtentication.strategy.jwt import JWTStrategy
from euro_cert_api.models.user import User
from euro_cert_api.utils.password import PasswordHelper
from euro_cert_api.schemas.user import CreateUserSchema, UpdateUserSchema
from euro_cert_api.schemas.auth import AuthCredentials
from euro_cert_api.common import exceptions


IDType = UUID4

password_helper = PasswordHelper()
josh_password_hash = password_helper.hash_password('12Qwerty!@')
elisabeth_password_hash = password_helper.hash_password('elisabeth')
paul_password_hash = password_helper.hash_password('paulo2134')


@dataclasses.dataclass
class UserModel:
    email: str
    hashed_password: str
    id: IDType = dataclasses.field(default_factory=uuid.uuid4)
    is_active: bool = True



class MockTransport(Transport):
    def __init__(self, tokenUrl: str):
        super().__init__(tokenUrl)


class MockStrategy(JWTStrategy):

    async def read_token(self, token: Optional[str], user_manager: UserManager) -> Optional[User]:
        if token is not None:
            try:
                parsed_id = user_manager.parse_id(token)
                return await user_manager.get_by_id(parsed_id)
            except Exception:
                return None
        return None

    async def write_token(self, user: UserModel):
        return str(user.id)

    async def destroy_token(self, token: str) -> None:
        return None


class MockUserManager(UserManager):
    async def _validate_password(self, password: str) -> None:
        if len(password) < 4:
            raise exceptions.InvalidPasswordException(
                "Password must be at least 4 characters long."
            )

    async def create_user(self, create_user: CreateUserSchema) -> UserModel:
        await self._validate_password(create_user.password)
        return UserModel(
            email=create_user.email,
            hashed_password=self.password_helper.hash_password(create_user.password),
            )

    async def update(self, user_update: UpdateUserSchema, user: UserModel) -> UserModel:
        pass

    async def delete(self, user: UserModel) -> UserModel:
        pass

    async def authenticate(
            self,
            credentials: AuthCredentials
    ) -> Optional[UserModel]:
        await self._validate_password(credentials.password)
        return UserModel(
            email=credentials.email,
            hashed_password=self.password_helper.hash_password(credentials.password),
        )


@pytest.fixture
def strategy() -> JWTStrategy:
    return MockStrategy(
        "secret",
        60*60*24
    )


@pytest.fixture
def transport() -> Transport:
    return MockTransport(
        "test/auth"
    )


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
        hashed_password=josh_password_hash
    )


@pytest.fixture
def inactive_user() -> UserModel:
    return UserModel(
        email='elisabeth_test_email@test.com',
        hashed_password=elisabeth_password_hash,
        is_active=False
    )


