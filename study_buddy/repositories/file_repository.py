import json

from bson import ObjectId

from study_buddy.models.file import File
from study_buddy.utils.database import file_collection


def save(file: File):
    new_file = file_collection.insert_one(
        json.loads(file.model_dump(exclude={"id"}))
    )
    return str(new_file.inserted_id)


def find_by_name(name: str) -> File | None:
    file = file_collection.find_one({"path": name})

    if not file:
        return None

    return File(**file)


def find_by_id(_id: str) -> File | None:
    file = file_collection.find_one({"_id": ObjectId(_id)})
    if not file:
        return None

    return File(**file)


def update(file: File):
    file_collection.update_one(
        {"_id": ObjectId(file.id)},
        {"$set": json.loads(file.model_dump(exclude={"id"}))},
    )
