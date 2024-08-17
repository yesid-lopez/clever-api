from dotenv import load_dotenv
from fastapi import FastAPI

from study_buddy.routers import health_router

load_dotenv()
study_buddy = "study_buddy".upper()
app = FastAPI(title=study_buddy, version="0.1.0")

app.include_router(health_router.router, tags=["health"])
