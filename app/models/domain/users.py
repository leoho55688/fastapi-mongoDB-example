from typing import Optional

from app.services.security import generate_salt, verify_password, get_password_hash
from app.models.common import DateTimeModelMixin, IDModelMixin
from app.models.domain.rwmodel import RWModel
from app.models.domain.mongo_model import MongoModel

class User(RWModel):
    username: str
    email: str
    bio: str = ""
    image: Optional[str] = None

class UserInDB(DateTimeModelMixin, IDModelMixin, MongoModel, User):
    salt: str = ""
    hashed_password: str = ""

    def check_password(self, password: str) -> bool:
        return verify_password(self.salt + password, self.hashed_password)
    
    def change_password(self, password: str) -> None:
        self.salt = generate_salt()
        self.hashed_password = get_password_hash(self.salt + password)