from fastapi import APIRouter, File, HTTPException, UploadFile

from study_buddy.services import file_service

router = APIRouter()


@router.post("/file", tags=["File"])
def upload_file(file: UploadFile = File(...)):
    blob_path, uri = file_service.upload_file(file)
    file_id = file_service.save_file(file.filename, blob_path, uri)
    created_file = file_service.find_file(file_id)
    return {
        "file_id": created_file.id,
        "type": created_file.type,
        "name": created_file.name,
    }


@router.get("/file", tags=["File"])
def find_file(name: str = None, file_id: str = None):
    file = file_service.find_file(file_id)

    if not file:
        file = file_service.find_file_by_name(name)

    if not file:
        raise HTTPException(status_code=404, detail="File not found")

    return file
