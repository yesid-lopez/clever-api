from typing import Optional, Any

from pydantic import BaseModel, field_validator, Field


class Question(BaseModel):
    id: Optional[Any] = Field(alias="_id", default=None)
    question: str
    answer: str
    course_id: Optional[str] = Field(default=None)

    @field_validator("id")
    def validate_id(cls, v):
        return str(v)
