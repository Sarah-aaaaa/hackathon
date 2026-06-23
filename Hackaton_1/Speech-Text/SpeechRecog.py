import speech_recognition as sr
from pydub import AudioSegment
audio = AudioSegment.from_mp3("May_Aud1.mp3")
audio.export("May_Aud1.wav", format="wav")

recognizer = sr.Recognizer()
filename = "May_Aud1.wav"

with sr.AudioFile(filename) as source:
    print("Reading audio...")
    audio_data = recognizer.record(source)

try:
    print("\nRecognized Text:")
    text = recognizer.recognize_google(audio_data)
    print(text)

except sr.UnknownValueError:
    print("Sorry, could not understand the audio.")
except sr.RequestError:
    print("Could not connect to Google API.")