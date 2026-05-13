#pip install pyttsx3
import pyttsx3
txt_sp=pyttsx3.init()
text=input("Enter the text:")
txt_sp.say(text)
txt_sp.runAndWait()