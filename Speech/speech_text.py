#pip install pyaudio
import pyaudio
#pip install SpeechRecognition
import speech_recognition as sr
def SpeechText():
    r=sr.Recognizer()
    mic=sr.Microphone()
    while True:
        with mic as source:
            print("Speak.......")
            audio=r.listen(source)
            try:
                text=r.recognize_google(audio)
                print(text)
                break
            except:
                print("No voice detected try again and speak louder...")
SpeechText()