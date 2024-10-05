# record_audio.py

import pyaudio
import wave


# Audio settings (constant values)
FORMAT = pyaudio.paInt16  # 16-bit audio format
CHANNELS = 1              # Mono sound
RATE = 44100              # Sampling rate (44.1 kHz)
CHUNK = 1024              # Buffer size

# Function to initialize and start the audio stream
def start_stream():
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)
    return p, stream

# Function to record audio
def record_audio_pls(stream, record_seconds):
    frames = []
    for _ in range(0, int(RATE / CHUNK * record_seconds)):
        data = stream.read(CHUNK)
        frames.append(data)
    return frames

# Function to save the recorded audio to a WAV file
def save_audio(p, frames, output_filename):
    wf = wave.open(output_filename, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()
