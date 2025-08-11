from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie

from euro_cert_api.models.user import User
from euro_cert_api.models.blacklist_token import BlacklistToken
from euro_cert_api.config import MONGO_URL, DB_NAME


async def reset_db():
    """
    Resets whole database
    """

    collections = [User, BlacklistToken]
    client = AsyncIOMotorClient(MONGO_URL)

    await client.drop_database(DB_NAME)
    print("Deleted {} database".format(DB_NAME))

    db = client[DB_NAME]
    await init_beanie(database=db, document_models=collections)
    print("Beanie initialized.")

    for collection in collections:
        await db.create_collection(collection.get_collection_name())
        print("Collection {} created.".format(collection.get_collection_name()))


async def init_db():
    client = AsyncIOMotorClient(MONGO_URL)
    db = client["euro_cert"]
    await init_beanie(
        database=db,
        document_models=[User, BlacklistToken]
    )
