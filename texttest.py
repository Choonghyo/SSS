import yt_dlp
from pydub import AudioSegment
import io
from google.cloud import speech_v1p1beta1 as speech
import os
from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse

# Google Cloud 인증 키 설정
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "C:/Users/KCH/Downloads/movie-ticket-sjle-cd0cffecadee.json"

# 전역 변수로 변환된 자막 텍스트를 저장
transcript_text = ""

class SubtitleRequestHandler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200, "ok")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "*")
        self.end_headers()

    def do_GET(self):
        if self.path == "/get_subtitle":
            self.send_response(200)
            self.send_header("Content-type", "text/plain; charset=utf-8")
            self.send_header("Access-Control-Allow-Origin", "*")  # CORS 문제 해결을 위한 헤더 추가
            self.end_headers()

            global transcript_text
            self.wfile.write(transcript_text.encode('utf-8'))

    def do_POST(self):
        if self.path == "/process_url":
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            post_data = urllib.parse.parse_qs(post_data.decode('utf-8'))
            youtube_url = post_data.get('url', [None])[0]
            
            if youtube_url:
                # YouTube URL 처리 및 텍스트 추출
                global transcript_text
                transcript_text = process_youtube_url(youtube_url)
                self.send_response(200)
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(b"Processing complete")
            else:
                self.send_response(400)
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(b"Invalid URL")

def process_youtube_url(youtube_url):
    # 1. YouTube에서 오디오 다운로드
    audio_file = download_audio_from_youtube(youtube_url, "audio")

    if audio_file is None:
        return "Failed to download audio."

    # 2. 모노로 변환
    print("Converting to mono...")
    mono_audio_file = convert_to_mono(audio_file)

    # 3. 오디오를 텍스트로 변환
    print("Transcribing audio to English text...")
    english_text = transcribe_audio(mono_audio_file)
    print("English Text:", english_text)
    
    return english_text

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

def run_http_server():
    server_address = ('', 8080)  # 로컬 호스트의 8080 포트에서 서버 실행
    httpd = HTTPServer(server_address, SubtitleRequestHandler)
    print("HTTP Server Running...")
    httpd.serve_forever()

if __name__ == "__main__":
    run_http_server()
