import os
from logging import getLogger

from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()
logger = getLogger(__name__)

MONGO_DETAILS = os.getenv(
    "MONGODB_URL", "mongodb://root:example@localhost:27017/"
)

print(MONGO_DETAILS)
logger.info(f"Connecting to MongoDB at {MONGO_DETAILS}")
client = MongoClient(MONGO_DETAILS)

database = client.study_buddy

course_collection = database.course
file_collection = database.file
question_collection = database.question
flashcard_collection = database.flashcard
