from bson import ObjectId
import logging

from motor.motor_asyncio import AsyncIOMotorClient

from app.db.collections.base import BaseCollection
from app.db.errors import EntityDoesNotExist
from app.models.domain.jobs import Job, JobInDB

class JobCollection(BaseCollection):
    def __init__(self, conn: AsyncIOMotorClient) -> None:
        super().__init__(conn=conn)
        self.__db_collection = "Job"

    async def get_job_by_id(self, *, id: str) -> JobInDB:
        job = await self._conn[self.__db_collection].find_one({
            "_id": ObjectId(id)
        })
        if job:
            return JobInDB.from_mongo(job)
        
        return EntityDoesNotExist(f"job with id: {id} does not exist")
    
    async def create_job(
        self,
        *,
        job_name: str,
        job_nature: str,
        job_requirement: str,
        job_description: str,
        password: str,
        uid: str
    ) -> JobInDB:
        job = JobInDB(
            job_name=job_name,
            job_nature=job_nature,
            job_requirement=job_requirement,
            job_description=job_description,
            uid=ObjectId(uid)
        )
        job.change_password(password)

        try:
            result = await self._conn[self.__db_collection].insert_one(job.mongo())
        except Exception as e:
            logging.exception(f"fail to inert document to mongo: {e}")
            raise

        return str(result.inserted_id)