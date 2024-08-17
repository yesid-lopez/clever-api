from typing import Optional

from fastapi import UploadFile
from google.cloud import storage

from study_buddy.models.file import File
from study_buddy.repositories import file_repository

bucket_name = "study-buddy-files"


def get_bucket():
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    return bucket


def upload_file(file: UploadFile):
    blob_name = format_name(file.filename)
    blob = get_bucket().blob(blob_name)
    content = file.file.read()
    blob.upload_from_string(content, content_type=file.content_type)

    return blob_name, _get_uri(blob.public_url)


def _get_uri(public_url: str):
    return public_url.replace("https://storage.googleapis.com/", "gs://")


def save_file(name: str, path: str, uri: str):
    file = File(
        path=path,
        name="".join(name.split(".")[:-1]),
        uri=uri,
        type=get_type(path),
    )
    file_id = file_repository.save(file)
    return file_id


def get_type(path):
    file_extension = path.split(".")[-1].lower()
    if file_extension in ["pdf"]:
        return "pdf"
    elif file_extension in ["jpg", "jpeg", "png"]:
        return "image"
    elif file_extension in ["mp3", "wav", "mp4"]:
        return "audio"
    else:
        return "unsuported"


def find_file(_id: str) -> File | None:
    file = file_repository.find_by_id(_id)
    return file


def find_file_by_name(name: str) -> Optional[File]:
    file = file_repository.find_by_name(name)

    return file


def update_file(file: File):
    file_repository.update(file)


def format_name(name: str):
    return name.lower().replace(" ", "-")
