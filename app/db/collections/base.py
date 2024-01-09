from motor.motor_asyncio import AsyncIOMotorClient

class BaseCollection:
    def __init__(self, conn: AsyncIOMotorClient) -> None:
        self._conn = conn

    @property
    def connection(self) -> AsyncIOMotorClient:
        return self._conn