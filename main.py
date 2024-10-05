import whisper 
from typing import Any
import record_audio
import keyboard
import os 
from datetime import datetime

# Whisper available models
AVAILABLE_MODELS = ["tiny", "base", "small", "medium", "large", "turbo"]
MODEL = "small"

# Audio settings 
RECORD_SECONDS = 5        # Duration of the recording

# constants used for naming the recorded audio
CUR_DIR = os.getcwd()




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
    if model not in AVAILABLE_MODELS:
        raise ValueError(f"Invalid model name {model}.")
    
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


def spacebar_was_pressed(model_instance):
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
    
    print(transcribe_audio(model_instance, file_path))


def run():
    # loads the whisper model once
    model_instance = load_model(MODEL)
    keyboard.on_press_key("space", lambda _ : spacebar_was_pressed(model_instance))
    # loops until 'esc' key is pressed. 
    keyboard.wait("esc")


if __name__ == "__main__":
    run()