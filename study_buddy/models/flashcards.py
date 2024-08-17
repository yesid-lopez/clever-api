from typing import Optional, Any

from pydantic import BaseModel, field_validator, Field


class Flashcard(BaseModel):
    id: Optional[Any] = Field(alias="_id", default=None)
    back: str
    front: str
    course_id: str

    @field_validator("id")
    def validate_id(cls, v):
        return str(v)


class Flashcards(BaseModel):
    flash_cards: list[Flashcard]


class RawFlashcard(BaseModel):
    front: str
    back: str


class RawFlashcards(BaseModel):
    flash_cards: list[RawFlashcard] = []
