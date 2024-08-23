import os

from pymongo import MongoClient

MONGO_DETAILS = os.getenv(
    "MONGODB_URL", "mongodb://root:example@localhost:27017/"
)

client = MongoClient(MONGO_DETAILS)

database = client.clever

course_collection = database.course
file_collection = database.file
question_collection = database.question
flashcard_collection = database.flashcard
