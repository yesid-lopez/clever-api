from fastapi import APIRouter

router = APIRouter()


@router.post("/health")
def health():
    return {"status": "ok"}
