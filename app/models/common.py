from typing import Annotated
from datetime import datetime
from bson import ObjectId

from pydantic import BaseModel, Field, field_validator

class DateTimeModelMixin(BaseModel):
    created_at: Annotated[datetime, Field(validate_default=True)] = None
    updated_at: Annotated[datetime, Field(validate_default=True)] = None

    @field_validator("created_at", "updated_at", mode="before")
    @classmethod
    def default_datetime(
        cls,
        value: datetime = None,
    ) -> datetime:
        return value or datetime.now()
    
class IDModelMixin(BaseModel):
    id: str = None