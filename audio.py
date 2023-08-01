import sounddevice as sd
from scipy.io import wavfile
import whisper
import numpy as np

model = whisper.load_model("small.en")


def capture_audio(duration=5, sample_rate=16000):
    # Start recording audio from the microphone
    audio_data = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1)
    sd.wait()  # Wait for the recording to complete
    # np.savetxt("file1.txt", audio_data)
    audio_waveform = np.squeeze(audio_data)
    transcription = model.transcribe(audio_waveform)

    dta = transcription["text"]
    print(dta)
    return dta

capture_audio(5,16000)