from bson import ObjectId
from typing import List
import logging

from motor.motor_asyncio import AsyncIOMotorClient

from app.db.collections.base import BaseCollection
from app.db.errors import EntityDoesNotExist
from app.models.domain.interviews import Interview, InterviewInDB

class InterviewCollection(BaseCollection):
    def __init__(self, conn: AsyncIOMotorClient) -> None:
        super().__init__(conn=conn)
        self.__db_collection = "Interview"

    async def get_interview_by_id(self, *, id: str) -> InterviewInDB:
        interview = await self._conn[self.__db_collection].find_one({
            "_id": ObjectId(id)
        })
        if interview:
            return InterviewInDB.from_mongo(interview)
        
        return EntityDoesNotExist(f"interview with id: {id} does not exist")
    
    async def get_interview_by_uId_jId(self, *, uId: str, jId: str) -> InterviewInDB:
        interview = await self._conn[self.__db_collection].find_one({
            "$and": [
                {"uId": uId},
                {"jId": jId}
            ]
        })
        if interview:
            return InterviewInDB.from_mongo(interview)
        
        return EntityDoesNotExist(f"interview with id: {id} does not exist")
    
    async def create_interview(
        self, 
        *,
        uId: str,
        jId: str,
        content: List[dict]
    ) -> InterviewInDB:
        interview = InterviewInDB(
            uId=uId,
            jId=jId,
            content=content
        )

        try:
            result = await self._conn[self.__db_collection].insert_one(interview.mongo())
        except Exception as e:
            logging.exception(f"fail to inert document to mongo: {e}")
            raise

        return str(result.inserted_id)