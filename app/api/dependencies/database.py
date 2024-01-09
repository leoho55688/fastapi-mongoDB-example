from typing import Callable, Type

from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorClient

from app.db.collections.base import BaseCollection
from app.db.events import get_db

def get_collection(
    col_type: Type[BaseCollection],
) -> Callable[[AsyncIOMotorClient], BaseCollection]:
    def _get_col(
        conn: AsyncIOMotorClient = Depends(get_db)
    ) -> BaseCollection:
        return col_type(conn=conn)
    
    return _get_col