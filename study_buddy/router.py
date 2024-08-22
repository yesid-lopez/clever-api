from dotenv import load_dotenv
from fastapi import FastAPI

from study_buddy.routers import (
    ai_router,
    course_router,
    file_router,
    flashcards_router,
    health_router,
    question_router,
)

load_dotenv()


study_buddy = "Clever".upper()
app = FastAPI(title=study_buddy, version="0.1.0")

app.include_router(health_router.router, tags=["Health"])
app.include_router(ai_router.router, tags=["AI"])
app.include_router(course_router.router, tags=["Course"])
app.include_router(flashcards_router.router, tags=["Flashcards"])
app.include_router(file_router.router, tags=["File"])
app.include_router(question_router.router, tags=["Question"])
