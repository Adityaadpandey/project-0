import sounddevice as sd
import numpy as np
import whisper
import bot
import pyttsx3

engine = pyttsx3.init()
model = whisper.load_model("small.en")

def speak(text):
    engine.say(text)
    engine.runAndWait()


def capture_audio(duration=5, sample_rate=16000):
    # Start recording audio from the microphone
    audio_data = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1)
    sd.wait()  # Wait for the recording to complete
    
    # Extract audio waveform
    audio_waveform = np.squeeze(audio_data)
    
    # Transcribe the audio to text
    transcription = model.transcribe(audio_waveform)
    text = transcription["text"]
    print("Transcription:", text)
    return text

# Set keyword and threshold for detection
keyword = ""
threshold = 0.01

# Initialize listening loop
while True:
    # Wait for the keyword to be spoken
    # input("Press Enter to start listening...")
    
    # Capture audio and perform translation
    audio_text = capture_audio()
    
    # Check if the keyword is present in the captured text
    if keyword in audio_text.lower():
        print("Keyword detected. Start translation.")
        translation = bot.chatbot(audio_text)
        speak(translation)
        #  = audio_text.replace(keyword,'')  # Add your translation logic here

        print("Translation:", translation)
    else:
        print("Keyword not detected.")
