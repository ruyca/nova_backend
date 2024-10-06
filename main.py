import whisper 
import record_audio
import keyboard
import os 
from datetime import datetime
from typing import Any
from openai_logic import query_chatgpt, voice_response, query_chatgpt2
from pydub import AudioSegment
from pydub.playback import play
import socketio

# Whisper available models
AVAILABLE_MODELS = ["tiny", "base", "small", "medium", "large", "turbo"]
EN_MODELS = ["tiny.en", "base.en", "small.en", "medium.en"]
MODEL = "base.en"

# Audio settings 
RECORD_SECONDS = 5      # Duration of the recording

# constants used for naming the recorded audio
CUR_DIR = os.getcwd()


sio = socketio.Client(logger=True, engineio_logger=True)

@sio.event
def connect():
    print("Connected to WebSocket server")

@sio.event
def connect_error(data):
    print(f"Connection failed: {data}")

@sio.event
def disconnect():
    print("Disconnected from WebSocket server")


def connect_to_socket():
    retries = 3
    for i in range(retries):
        try:
            if not sio.connected:
                sio.connect('http://localhost:5000', wait_timeout=10)
                return True
        except Exception as e:
            print(f"Connection attempt {i+1} failed: {e}")
            if i < retries - 1:  # Don't sleep after the last attempt
                time.sleep(2)
    return False


def load_model(model: str) -> Any:
    """
    Loads one of the models available for Whisper: 
        1. tiny 
        2. base
        3. small
        4. medium
        5. large
        6. turbo 
    Accuary increases for larger models, but so does 
    the requiered VRAM. 

    Returns the object. 
    """
    #if (model not in AVAILABLE_MODELS) or (model not in EN_MODELS):
    #    raise ValueError(f"Invalid model name {model}.")
    
    model_instance = whisper.load_model(model)
    
    return model_instance

def transcribe_audio(model: Any, aupath: str) -> str: 
    """
    Transcribes the audio and returns the text from the audipath.
    """
    
    print("\n\n")
    print(f"Loading audio from: {aupath}")
    result = model.transcribe(aupath)
    text = result["text"]
    
    return text

def generate_filename() -> str:
    """
    Names the current audiofile generated
    """
    timestamp = datetime.now().strftime("%d%m%Y_%H%M%S")
    filename = f"recording_{timestamp}.wav"

    return filename

def play_audio(file_path: str): 
    audio = AudioSegment.from_file(file_path)

    # play the audio file
    play(audio)


def stream_audio():

    p, stream = record_audio.start_stream()  # Start the audio stream
    print("Recording...")
    frames = record_audio.record_audio_pls(stream, RECORD_SECONDS)  # Record audio
    print("Finished recording.")
    
    # Stop and close the stream
    stream.stop_stream()
    stream.close()
    p.terminate()
    
    file_name = generate_filename()
    target_dir = os.path.join(CUR_DIR, "audios")
    # Creates the audio dir. Doesn't raise error if already exists
    os.makedirs(target_dir, exist_ok=True)

    file_path = os.path.join(target_dir, file_name)

    # Save the recorded audio
    record_audio.save_audio(p, frames, file_path)
    print(f"Audio saved as {file_name}")

    return file_path

def extract_celestial_body(text):
    # This is a simple example. You might need more sophisticated logic
    celestial_bodies = ['mercury', 'venus', 'earth', 'moon', 'mars', 
                        'jupiter', 'saturn', 'uranus', 'neptune', 'sun']
    
    for body in celestial_bodies:
        if body in text:
            return body
        
    
    return None

def spacebar_was_pressed(model_instance):
    file_path = stream_audio()
    audio_trans = transcribe_audio(model_instance, file_path)
    print(f"AUDIO TRANS:\n{audio_trans}")
    # Extract the celestial body from the transcription
    # You might need to implement logic to extract the specific celestial body name
    celestial_body = extract_celestial_body(audio_trans.lower())
    print(celestial_body)
    if celestial_body:
        try:
            # Emit the celestial body to the WebSocket server
            sio.emit('celestial_body_selected', {'body': celestial_body})
            print(f"Sent celestial body: {celestial_body} to frontend")
        except Exception as e:
            print(f"Failed to send celestial body: {e}")

    # Continue with your existing logic
    celestial_body, msg_info = query_chatgpt(celestial_body=audio_trans)
    audio_response_path = voice_response(msg_info=msg_info)
    play_audio(audio_response_path)

    #

def run():
    connect_to_socket()
    # loads the whisper model once
    model_instance = load_model(MODEL)
    play_audio("agent_answers\prerecorded\intro2_fav.wav")

    # ANSWER MODE: 
    #   1 -> Basic information. 
    #   2 -> Query information (which is bigger, etc)
    

    keyboard.on_press_key("space", lambda _ : spacebar_was_pressed(model_instance))
    # loops until 'esc' key is pressed. 
    keyboard.wait("esc")


if __name__ == "__main__":
    run()