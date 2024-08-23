from typing import Any, Optional

from pydantic import BaseModel, Field, field_validator


class Course(BaseModel):
    id: Optional[Any] = Field(alias="_id", default=None)
    name: str
    files: list[str]

    class Config:
        json_schema_extra = {
            "example": {
                "name": "History of Computers",
                "files": ["656b599eb8a5f633adf7eab9"],
            }
        }

    @field_validator("id")
    def validate_id(cls, v):
        return str(v)
