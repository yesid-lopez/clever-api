from os import environ
from typing import Optional

from fastapi import UploadFile
from minio import Minio

from study_buddy.models.file import File
from study_buddy.repositories import file_repository

bucket_name = "study-buddy-files"


def get_minio_client():
    endpoint = environ.get("MINIO_ENDPOINT")
    access_key = environ.get("MINIO_ACCESS_KEY")
    secret_key = environ.get("MINIO_SECRET_KEY")
    secure = environ.get("MINIO_SECURE")
    minio_client = Minio(
        endpoint,
        access_key=access_key,
        secret_key=secret_key,
        secure=True if secure == "True" else False,
    )
    return minio_client


def upload_file(file: UploadFile):
    bucket_name = environ.get("MINIO_BUCKET_NAME")
    blob_name = format_name(file.filename)
    minio_client = get_minio_client()
    content = file.file
    minio_client.put_object(bucket_name, blob_name, content,
                            file.size,)
    return blob_name


def save_file(name: str, path: str):
    file = File(
        path=path,
        name="".join(name.split(".")[:-1]),
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
