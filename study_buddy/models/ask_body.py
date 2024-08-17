from pydantic import BaseModel


class AskBody(BaseModel):
    question: str
    course_id: str
    files: list[str]

    class Config:
        schema_extra = {
            "example": {
                "course_id": "656b599eb8a5f633adf7eab9",
                "files": ["656b599eb8a5f633adf7eab9"],
                "question": "What was the first computer?",
            }
        }
