# Nova - Your Virtual Assistant for Celestial Exploration
**Nova** is a virtual assistant designed to help users learn about celestial bodies in our galaxy, 
particularly those within our solar system. The project utilizes voice recognition, the ChatGPT API, 
and text-to-speech technology to provide users with an interactive and engaging learning experience about space.

**Nova** listens to the user’s voice, processes their questions, retrieves relevant information via the ChatGPT API,
and then speaks the answers back using synthesized voice. Additionally, Nova displays images of the celestial body the user 
wants to learn about on the frontend.

## Features
- **Voice Input**: Nova uses speech recognition to interpret user queries about celestial bodies.
- **ChatGPT Integration**: Once the voice input is processed into text, Nova queries the ChatGPT API to retrieve relevant information.
- **Voice Output**: Nova responds to the user by converting the information retrieved from ChatGPT back into speech using text-to-speech
  technology.
- **Celestial Body Visualization**: After querying ChatGPT, Nova sends the name of the celestial body to the frontend, where an image of the object is displayed.
 
## Technologies and Libraries
This project uses a variety of Python libraries to achieve voice recognition, API interactions, and audio playback. 
Below is a breakdown of the libraries used in each module:

### In `main.py`
- `whisper`: For speech-to-text conversion.
- `record_audio`: Captures and processes the user's voice input.
- `keyboard`: Allows the program to detect keyboard events.
- `os`: Used for various system-level operations like accessing environment variables.
- `datetime`: Handles date and time operations.
- `typing`: Provides type hinting for function signatures.
- `openai_logic`: Contains functions to query ChatGPT and generate voice responses.
- `pydub`: Handles audio playback functionality.


### In `openai_logic.py`
- `dotenv`: Loads environment variables, specifically for securely managing the ChatGPT API key.
- `openai`: Used for interacting with OpenAI’s API to query ChatGPT.
- `datetime`: Used for logging and time-related operations.
- `random`: To randomly select from various potential responses.
- `os`: To access environment variables and system functions.

### In `record_audio.py`
- `pyaudio`: Captures audio from the user's microphone.
- `wave`: Handles audio file reading and writing.


## API Key Management
To protect the API keys and sensitive information, this project uses the dotenv library. 
Ensure you have a .env file that contains the following environment variable:

```bash
OPENAI_API_KEY=your_openai_api_key_here
```

## Installation
1. Clone the repository:
```bash
git clone https://github.com/ruyca/nova-backend.git
cd nova-backend
```

2. Install the required Python libraries:
```bash
pip install -r requirements.txt
```
3. Set up your .env file with your OpenAI API key.
```bash
echo "OPENAI_API_KEY=your_openai_api_key_here" > .env
```

4. Run the project:

```bash
python main.py
```

## Usage
- Nova will listen to your voice commands, such as asking for information about planets, stars, or other celestial objects.
- Once the query is received, Nova will fetch information from ChatGPT and respond with both spoken words and an image of the celestial body.

## Contributing
We welcome contributions! If you’d like to contribute to Nova, please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Make your changes and commit them.
4. Open a pull request detailing the changes you’ve made.

   
## License
This project is licensed under the MIT License. See the LICENSE file for details.
