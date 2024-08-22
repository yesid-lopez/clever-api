from typing import Any, Optional

from pydantic import BaseModel, Field, field_validator


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
    """Data model for a Flashcard"""

    front: str
    back: str


class RawFlashcards(BaseModel):
    flash_cards: list[RawFlashcard] = []
