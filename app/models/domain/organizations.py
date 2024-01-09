from app.services.security import generate_salt, verify_password, get_password_hash
from app.models.common import DateTimeModelMixin, IDModelMixin
from app.models.domain.rwmodel import RWModel
from app.models.domain.mongo_model import MongoModel

class Organization(RWModel):
    organization_name: str

class OrganizationInDB(DateTimeModelMixin, IDModelMixin, MongoModel, Organization):
    salt: str = ""
    hashed_password: str = ""

    def check_password(self, password: str) -> bool:
        return verify_password(self.salt + password, self.hashed_password)
    
    def change_password(self, password: str) -> None:
        self.salt = generate_salt()
        self.hashed_password = get_password_hash(self.salt + password)