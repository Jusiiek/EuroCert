import json

from euro_cert_api.config import FIXTURES_PATH
from euro_cert_api.managers.user import UserManager
from euro_cert_api.schemas.user import CreateUserSchema


async def load_users():
    user_manager = UserManager()

    with open(f'{FIXTURES_PATH}/users.json') as f:
        users = json.load(f)

    for user in users:
        create_schema = CreateUserSchema(**user)
        await user_manager.create(create_schema)
