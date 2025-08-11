import motor.motor_asyncio
from beanie import init_beanie

from euro_cert_api.models.user import User
from euro_cert_api.models.blacklist_token import BlacklistToken
from euro_cert_api.config import MONGO_URL


async def init_db():
    client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URL)
    await init_beanie(
        database=client.euro_cert_db,
        document_models=[User, BlacklistToken]
    )
