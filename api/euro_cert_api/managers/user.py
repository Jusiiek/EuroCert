import re

from typing import Any, Optional
from bson import ObjectId

from euro_cert_api.models.user import User
from euro_cert_api.utils.password import PasswordHelper


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
            raise Exception(f"User {user_id} not found")

        return user

    async def get_by_email(self, email: str) -> Optional[User]:
        user: Optional[User] = await User.get_by_email(email)
        if user is None:
            raise Exception(f"User with email {email} not found")

        return user

    async def create(self, user_create: dict) -> User:
        pass

    async def update(self, update_dict: dict, user: User) -> User:
        pass

    async def delete(self, user: User) -> None:
        return await user.delete()

    async def authenticate(
            self,
            credentials: dict
    ) -> Optional[User]:
        pass
