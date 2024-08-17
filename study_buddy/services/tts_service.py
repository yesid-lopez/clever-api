import io

# from google.cloud import texttospeech


def get_speech(message: str):
    # client = texttospeech.TextToSpeechClient()
    # input_text = texttospeech.SynthesisInput(text=message)

    # # Configure the voice settings
    # voice = texttospeech.VoiceSelectionParams(
    #     language_code="en-US", ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
    # )

    # # Set the audio configuration
    # audio_config = texttospeech.AudioConfig(
    #     audio_encoding=texttospeech.AudioEncoding.MP3
    # )

    # # Perform the text-to-speech request
    # response = client.synthesize_speech(
    #     input=input_text, voice=voice, audio_config=audio_config
    # )
    # return response
    pass


def convert_stream(audio_content: bytes):
    return io.BytesIO(audio_content)
