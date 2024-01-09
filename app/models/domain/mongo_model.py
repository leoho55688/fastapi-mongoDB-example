from bson import ObjectId

from pydantic import BaseModel

class MongoModel(BaseModel):
    @classmethod
    def from_mongo(cls, data: dict):
        if not data:
            return data
        id = str(data.pop("_id", None))
        return cls(**data, id=id)

    def mongo(self, **kwargs):
        exclude_unset = kwargs.pop("exclude_unset", False)
        by_alias = kwargs.pop("by_alias", True)

        parsed = self.model_dump(
            exclude_unset=exclude_unset,
            by_alias=by_alias,
            **kwargs
        )

        if "_id" not in parsed and "id" in parsed:
            parsed["_id"] = ObjectId(parsed.pop("id"))

        return parsed