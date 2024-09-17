import librosa

audio_file = 'static/aud.wav'
try:
    y, sr = librosa.load(audio_file, sr=None)
    print(f"Loaded audio with shape: {y.shape}, sample rate: {sr}")
except Exception as e:
    print(f"Error loading audio file: {e}")