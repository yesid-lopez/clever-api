from os import environ

from fastapi import UploadFile
from minio import Minio

from clever.utils.formatter import format_file_name


class MinioClient:

    def __init__(self):
        self.load_minio_client()
        self.bucket_name = environ.get("MINIO_BUCKET_NAME")

    def load_minio_client(self):
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
        self.minio_client = minio_client

    def upload_file(self, file: UploadFile):
        blob_name = format_file_name(file.filename)
        content = file.file
        self.minio_client.put_object(
            self.bucket_name, blob_name, content, file.size
        )
        return blob_name

    def get_file(self, blob_name: str):
        return self.minio_client.get_object(self.bucket_name, blob_name)

    def fget_file(self, blob_name: str, file_path: str):
        return self.minio_client.fget_object(
            self.bucket_name, blob_name, file_path
        )
