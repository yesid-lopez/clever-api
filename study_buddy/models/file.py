from typing import Optional, Any

from pydantic import BaseModel, field_validator, Field


class File(BaseModel):
    id: Optional[Any] = Field(alias="_id", default=None)
    name: str
    type: str
    path: str
    embeddings_collection: Optional[str] = Field(default=None)
    uri: str

    @field_validator("id")
    def validate_id(cls, v):
        return str(v)
