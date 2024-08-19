import io
import os
from google.cloud import speech

# JSON 키 파일 경로 설정
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r"C:\Users\KCH\Downloads\movie-ticket-sjle-cd0cffecadee.json"

def transcribe_speech(audio_path):
    client = speech.SpeechClient()

    with io.open(audio_path, "rb") as audio_file:
        content = audio_file.read()

    audio = speech.RecognitionAudio(content=content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,  # 이 값을 오디오 파일에 맞게 설정하세요.
        language_code="ko-KR",  # 한국어로 인식하려면 이 값을 설정하세요.
    )

    response = client.recognize(config=config, audio=audio)

    for result in response.results:
        print("Transcript: {}".format(result.alternatives[0].transcript))

# 오디오 파일 경로 지정
transcribe_speech("path_to_your_audio_file.wav")
