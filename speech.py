import speech_recognition as sr

r = sr.Recognizer()

with sr.Microphone() as source:
    print("Speak:")
    audio = r.listen(source)

print(type(audio))
