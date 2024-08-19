import os
import io
from google.cloud import speech_v1p1beta1 as speech
from google.oauth2 import service_account
from pydub import AudioSegment
import yt_dlp as youtube_dl

def download_youtube_audio(youtube_url, output_path):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': output_path,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'wav',
            'preferredquality': '192',
        }],
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([youtube_url])

def transcribe_audio(audio_path, credentials_path):
    credentials = service_account.Credentials.from_service_account_file(credentials_path)
    client = speech.SpeechClient(credentials=credentials)

    with io.open(audio_path, "rb") as audio_file:
        content = audio_file.read()

    audio = speech.RecognitionAudio(content=content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code="ko-KR",  # 한국어, 영어의 경우 "en-US"
    )

    response = client.recognize(config=config, audio=audio)

    # 텍스트 출력
    for result in response.results:
        print("Transcript: {}".format(result.alternatives[0].transcript))

def main():
    youtube_url = "https://www.youtube.com/watch?v=X0mWbWRx-R0"  # 사용할 YouTube URL
    audio_file = "audio.wav"  # 저장할 오디오 파일 이름
    credentials_path = "path/to/your/credentials.json"  # 서비스 계정 키 파일 경로

    print("Downloading YouTube video and extracting audio...")
    download_youtube_audio(youtube_url, audio_file)

    print("Transcribing audio using Google Cloud Speech-to-Text API...")
    transcribe_audio(audio_file, credentials_path)

if __name__ == "__main__":
    main()
