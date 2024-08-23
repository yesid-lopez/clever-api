from typing import Any, Optional

from pydantic import BaseModel, Field, field_validator


class File(BaseModel):
    id: Optional[Any] = Field(alias="_id", default=None)
    name: str
    type: str
    path: str
    embeddings_collection: Optional[str] = Field(default=None)

    @field_validator("id")
    def validate_id(cls, v):
        return str(v)
