from pydantic import BaseModel


class GenerateFlashcardsBody(BaseModel):
    course_id: str
    files: list[str]
    flashcards_per_file: int = 5
