import os
import json

from euro_cert_api.config import FIXTURES_PATH
from euro_cert_api.models.user import User
from euro_cert_api.utils.password import PasswordHelper


async def load_users():
    password_helper = PasswordHelper()

    with open(
        os.path.join(FIXTURES_PATH, "users.json")
    ) as f:
        users = json.load(f)

    for user in users:
        user["hashed_password"] = password_helper.hash_password(user["password"])
        del user["password"]
        user = User(**user)
        await user.insert()
