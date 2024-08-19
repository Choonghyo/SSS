import yt_dlp
from pydub import AudioSegment
import io
from google.cloud import speech_v1p1beta1 as speech
import os

# Google Cloud 인증 키 설정
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "C:/Users/KCH/Downloads/movie-ticket-sjle-cd0cffecadee.json"

def download_audio_from_youtube(youtube_url, output_path="audio.wav"):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': output_path,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'wav',
            'preferredquality': '192',
        }],
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([youtube_url])
        # 다운로드된 파일명을 정확히 확인하고 일치시킴
        downloaded_file = output_path + ".wav"
        if not os.path.exists(downloaded_file):
            raise FileNotFoundError(f"{downloaded_file} not found.")
        print(f"Downloaded audio to {downloaded_file}")
        return downloaded_file
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def convert_to_mono(audio_path):
    sound = AudioSegment.from_wav(audio_path)
    sound = sound.set_channels(1)  # 모노로 변환
    mono_path = audio_path.replace(".wav", "_mono.wav")
    sound.export(mono_path, format="wav")
    return mono_path

def transcribe_audio(audio_path):
    client = speech.SpeechClient()

    with io.open(audio_path, "rb") as audio_file:
        content = audio_file.read()

    audio = speech.RecognitionAudio(content=content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=48000,
        language_code="en-US",
    )

    response = client.recognize(config=config, audio=audio)

    transcript = ""
    for result in response.results:
        transcript += result.alternatives[0].transcript + " "
    
    return transcript

def main():
    youtube_url = "https://www.youtube.com/watch?v=X0mWbWRx-R0"
    
    # 1. YouTube에서 오디오 다운로드
    audio_file = download_audio_from_youtube(youtube_url, "audio")

    if audio_file is None:
        print("Failed to download audio.")
        return

    # 2. 모노로 변환
    print("Converting to mono...")
    mono_audio_file = convert_to_mono(audio_file)

    # 3. 오디오를 텍스트로 변환
    print("Transcribing audio to English text...")
    english_text = transcribe_audio(mono_audio_file)
    print("English Text:", english_text)

if __name__ == "__main__":
    main()
