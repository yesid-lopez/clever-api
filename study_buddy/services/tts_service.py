import io

from openai import OpenAI

client = OpenAI()


def get_speech(message: str):
    response = client.audio.speech.create(
        model="tts-1",
        voice="alloy",
        input=message
    )
    return response


def convert_stream(audio_content: bytes):
    return io.BytesIO(audio_content)
