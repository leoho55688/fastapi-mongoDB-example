from bson import ObjectId
import logging
from typing import Optional

from motor.motor_asyncio import AsyncIOMotorClient

from app.db.collections.base import BaseCollection
from app.db.errors import EntityDoesNotExist
from app.models.domain.users import User, UserInDB

class UserCollection(BaseCollection):
    def __init__(self, conn: AsyncIOMotorClient) -> None:
        super().__init__(conn=conn)
        self.__db_collection = "User"

    async def get_user_by_email(self, *, email: str) -> UserInDB:
        user = await self._conn[self.__db_collection].find_one({
            "email": email
        })
        if user:
            return UserInDB.from_mongo(user)
        
        raise EntityDoesNotExist(f"user with email: {email} does not exist")
    
    async def get_user_by_username(self, *, username: str) -> UserInDB:
        user = await self._conn[self.__db_collection].find_one({
            "username": username
        })
        if user:
            return UserInDB.from_mongo(user)
        
        raise EntityDoesNotExist(f"user with username: {username} does not exist")
    
    async def create_user(
        self,
        *,
        username: str,
        email: str,
        password: str,
    ) -> UserInDB:
        user = UserInDB(username=username, email=email)
        user.change_password(password=password)

        try:
            await self._conn[self.__db_collection].insert_one(user.mongo())
        except Exception as e:
            logging.exception(f"fail to inert document to mongo: {e}")
            raise

        return user
    
    async def update_user(
        self,
        *,
        user: User,
        username: Optional[str] = None,
        email: Optional[str] = None,
        password: Optional[str] = None,
        bio: Optional[str] = None,
        image: Optional[str] = None,
    ) -> UserInDB:
        user_in_db = await self.get_user_by_email(email=user.email)

        if not user_in_db:
            raise EntityDoesNotExist(f"user with email: {user.email} does not exist")

        user_in_db.username = username or user.username
        user_in_db.email = email or user.email
        user_in_db.bio = bio or user.bio
        user_in_db.image = image or user.image
        if password:
            user_in_db.change_password(password)

        print(email)

        try:
            await self._conn[self.__db_collection].find_one_and_update(
                {"_id": ObjectId(user_in_db.id)},
                {"$set": user_in_db.mongo()}
            )
        except Exception as e:
            logging.exception(f"fail to update document to mongodb: {e}")
            raise

        return user_in_db
