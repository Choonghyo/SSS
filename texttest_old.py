import yt_dlp
from pydub import AudioSegment
import io
from google.cloud import speech_v1p1beta1 as speech
import os
from http.server import BaseHTTPRequestHandler, HTTPServer

# Google Cloud 인증 키 설정
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "C:/Users/KCH/Downloads/movie-ticket-sjle-cd0cffecadee.json"

# HTTP 서버 핸들러
class SubtitleRequestHandler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200, "ok")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "*")
        self.end_headers()

    def do_GET(self):
        if self.path == "/get_subtitle":
            self.send_response(200)
            self.send_header("Content-type", "text/plain; charset=utf-8")
            self.send_header("Access-Control-Allow-Origin", "*")  # CORS 문제 해결을 위한 헤더 추가
            self.end_headers()

            # 여기서 변환된 자막 텍스트를 전송합니다.
            subtitle_text = self.server.transcript_text or "No subtitles available."
            self.wfile.write(subtitle_text.encode('utf-8'))

def run_http_server(transcript_text):
    server_address = ('', 8080)  # 로컬 호스트의 8080 포트에서 서버 실행
    httpd = HTTPServer(server_address, SubtitleRequestHandler)
    httpd.transcript_text = transcript_text  # 텍스트 저장
    print("HTTP Server Running...")
    httpd.serve_forever()

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
    
    # 4. HTTP 서버 실행
    run_http_server(english_text)

if __name__ == "__main__":
    main()
