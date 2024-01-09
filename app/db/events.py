from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient
import logging

from app.core.config import get_app_setting

load_dotenv()
settings = get_app_setting()

db_client: AsyncIOMotorClient = None

async def get_db() -> AsyncIOMotorClient:
    db_name = settings.database_name
    return db_client[db_name]

async def connect_and_init_db():
    global db_client
    try:
        db_client = AsyncIOMotorClient(
            settings.database_url,
            maxPoolSize=settings.max_connection_count,
            minPoolSize=settings.min_connection_count,
            uuidRepresentation="standard"
        )
        logging.info("Connected to mongo.")
    except Exception as e:
        logging.exception(f"Could not connect to mongo: {e}")
        raise

async def close_db_connection():
    global db_client
    if db_client is None:
        logging.warning("Connection is None, nothing to close.")
        return
    db_client.close()
    db_client = None
    logging.info("Mongo connection closed.")