from datetime import datetime, timezone
from typing import Any, Callable, Self

from pydantic import BaseModel, ConfigDict, model_serializer

def convert_field_to_camel_case(string: str) -> str:
    return "".join(
        word if index == 0 else word.capitalize()
        for index, word in enumerate(string.split("_"))
    )

class RWModel(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
        alias_generator=convert_field_to_camel_case
    )

    @model_serializer(mode="wrap")
    def serialize(self, original_serializer: Callable[[Self], dict[str, Any]]) -> dict[str, Any]:
        for field_name, field_info in self.model_fields.items():
            if field_info.annotation == datetime:
                setattr(self, field_name, getattr(self, field_name).replace(tzinfo=timezone.utc))

        result = original_serializer(self)

        return result