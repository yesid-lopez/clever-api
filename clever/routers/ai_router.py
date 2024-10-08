from fastapi import APIRouter
from fastapi.responses import Response, StreamingResponse

from clever.services import tts_service

router = APIRouter()


@router.get("/extract-text-from-image")
def get_text_from_image(uri: str):
    #     ocr_content = extract_text_from_uri(uri)
    #     return {"text": content.text}
    pass


@router.get("/text-to-speech/stream")
def stream_text_to_speech(message: str):
    audio = tts_service.get_speech(message)
    streaming_response = StreamingResponse(
        tts_service.convert_stream(audio.content), media_type="audio/wav"
    )
    return streaming_response


@router.get("/text-to-speech")
def text_to_speech(message: str):
    audio = tts_service.get_speech(message)
    return Response(content=audio.content, media_type="audio/wav")
