import speech_recognition as sr
from pydub import AudioSegment

# 오디오 파일을 로드합니다.
audio_file = "audio.wav"

# Recognizer 인스턴스를 만듭니다.
recognizer = sr.Recognizer()

# 오디오 파일을 읽습니다.
with sr.AudioFile(audio_file) as source:
    audio_data = recognizer.record(source)

# Google Web Speech API를 사용하여 텍스트를 추출합니다.
try:
    text = recognizer.recognize_google(audio_data)
    print("Extracted Text: ", text)
except sr.UnknownValueError:
    print("Google Web Speech API could not understand audio")
except sr.RequestError as e:
    print(f"Could not request results from Google Web Speech API; {e}")
