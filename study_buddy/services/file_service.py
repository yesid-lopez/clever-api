from typing import Optional

from fastapi import UploadFile

from study_buddy.clients.minio_client import MinioClient
from study_buddy.models.file import File
from study_buddy.repositories import file_repository


def upload_file(file: UploadFile):
    blob_name = MinioClient().upload_file(file)
    return blob_name


def save_file(name: str, path: str):
    file = File(
        path=path,
        name="-".join(name.split(".")[:-1]),
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
