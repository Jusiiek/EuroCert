import re

from typing import Optional
from bson import ObjectId

from euro_cert_api.models.user import User
from euro_cert_api.utils.password import PasswordHelper
from euro_cert_api.common import exceptions
from euro_cert_api.schemas.user import CreateUserSchema
from euro_cert_api.schemas.auth import AuthCredentials
from euro_cert_api.managers.base import BaseManager


class UserManager(BaseManager):

    def __init__(self, password_helper: PasswordHelper = None):
        super(self, UserManager).__init__()
        self.password_helper = password_helper or PasswordHelper()

    async def _validate_password(self, password: str) -> tuple[list, bool]:
        """

        Validates a password
        :param password: str - The password to validate
        :returns result: tuple[list, bool] list of errors, is_password_valid - The error list stores all
        the missing password features, is_password_valid is just a bool value if password is valid or not

        """
        errors = []

        if not re.search(r'[A-Z]', password):
            errors.append("Missing uppercase letter")

        if not re.search(r'[a-z]', password):
            errors.append("Missing lowercase letter")

        if not re.search(r'\d', password):
            errors.append("Missing digit")

        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            errors.append("Missing special character")

        if len(password) < 8:
            errors.append("Too short password. Minimum 8 characters")

        return errors, len(errors) == 0

    async def get_by_id(self, user_id: ObjectId) -> Optional[User]:
        user: Optional[User] = await User.get_by_id(user_id)
        if user is None:
            raise exceptions.UserNotExists()

        return user

    async def get_by_email(self, email: str) -> Optional[User]:
        user: Optional[User] = await User.get_by_email(email)
        if user is None:
            raise exceptions.UserNotExists()

        return user

    async def create(self, user_create: CreateUserSchema) -> User:
        errors, is_pass_valid = await self._validate_password(user_create.password)
        if not is_pass_valid:
            raise exceptions.InvalidPasswordException(', '.join(errors))

        try:
            await self.get_by_email(user_create.email)
            raise exceptions.UserAlreadyExists()
        except exceptions.UserNotExists:
            pass

        user_dict = user_create.create_update_dict()
        user_dict["hashed_password"] = self.password_helper.hash_password(user_create.password)
        del user_dict["password"]
        user = User(**user_dict)
        return await user.insert()

    async def authenticate(
            self,
            credentials: AuthCredentials
    ) -> Optional[User]:
        try:
            user: User = await self.get_by_email(credentials.email)
        except exceptions.UserNotExists:
            return None

        verified = self.password_helper.verify_password(
            credentials.password, user.hashed_password
        )
        if not verified:
            return None

        return user
