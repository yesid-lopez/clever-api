from typing import Optional, Any

from pydantic import BaseModel, field_validator, Field


class Course(BaseModel):
    id: Optional[Any] = Field(alias="_id", default=None)
    name: str
    files: list[str]

    class Config:
        schema_extra = {
            "example": {
                "name": "History of Computers",
                "files": ["656b599eb8a5f633adf7eab9"]
            }
        }

    @field_validator("id")
    def validate_id(cls, v):
        return str(v)
