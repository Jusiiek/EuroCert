import re

from typing import Any, Optional
from bson import ObjectId

from euro_cert_api.models.user import User
from euro_cert_api.utils.password import PasswordHelper
from euro_cert_api.common import exceptions
from euro_cert_api.schemas.user import (
    CreateUserSchema,
    UpdateUserSchema,
)
from euro_cert_api.schemas.auth import AuthCredentials


class UserManager:

    def __init__(self, password_helper: PasswordHelper = None):
        self.password_helper = password_helper or PasswordHelper()

    def parse_id(self, id: Any) -> ObjectId:
        """
        Parse a value into a correct ID type.

        Params
        -------------------
        id: Any - model id as different type

        Returns
        --------------
        id: ObjectId - Model correct ID
        """

        if isinstance(id, ObjectId):
            return id
        try:
            return ObjectId(id)
        except Exception as e:
            raise e

    async def _validate_password(self, password: str) -> tuple[list, bool]:
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

        if await self.get_by_email(user_create.email):
            raise exceptions.UserAlreadyExists()

        user_dict = user_create.create_update_dict()
        user_dict["hashed_password"] = self.password_helper.hash_password(user_create.password)
        del user_dict["password"]
        user = User(**user_dict)
        return await user.insert()

    async def update(self, user_update: UpdateUserSchema, user: User) -> User:
        update_dict = user_update.create_update_dict()

        for field, value in update_dict.items():
            if field == "email" and value != user.email:
                if await self.get_by_email(value):
                    raise exceptions.UserAlreadyExists()
                else:
                    setattr(user, field, value)
            elif field == "password" and value is not None:
                errors, is_pass_valid = await self._validate_password(value)
                if is_pass_valid:
                    hashed_pass = self.password_helper.hash_password(
                        value
                    )
                    setattr(user, "hashed_password", hashed_pass)
                else:
                    raise exceptions.InvalidPasswordException(', '.join(errors))
            else:
                setattr(user, field, value)
            await user.save()
            return user

    async def delete(self, user: User) -> None:
        return await user.delete()

    async def authenticate(
        self,
        credentials: AuthCredentials
    ) -> Optional[User]:
        pass
