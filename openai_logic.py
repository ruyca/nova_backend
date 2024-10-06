#  openai_logic.py
from dotenv import load_dotenv
from openai import OpenAI
from datetime import datetime
from random import choice
import os

# load env variables 
load_dotenv()
OPENAI_KEY = os.getenv("OPENAI_API")
OPTIONS = [
    "Please let me know if you would like to know more.",
    "Would you like to know more?",
    "Do you want me to explain further?"
]

def query_chatgpt(**kwargs):
    client = OpenAI(api_key=OPENAI_KEY)
    celestial_body = kwargs["celestial_body"]

    completion = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", 
        "content": "You are an astrophysics expert that brings relevant information \
            about celestial bodies. You explain the information in a short but \
            insightful way. Only respond with brief but insightful manner. The \
            user will tell you one celestial body on which you must provide the info.\
            Your answer shouldn't be any longer than 2 sentences."},
        {"role": "user", "content": f"Tell me about {celestial_body}"}
    ]
    )

    know_more = choice(OPTIONS)

    message = completion.choices[0].message.content
    message += know_more

    print(f"\n\n{message}\n\n")

    return message

def voice_response(**kwargs):
    print("THIS FUNCTION WAS RUUUHN")
    # Initialize the OpenAI client with the API key
    client = OpenAI(api_key=OPENAI_KEY)

    input_msg = kwargs["msg_info"]

    # Create the speech response from the input
    response = client.audio.speech.create(
        model="tts-1-hd",
        voice="nova",
        input=input_msg
    )

    # Define the directory where the file will be saved
    directory = "agent_answers"
    filename = f"response_{datetime.now().strftime('%Y%m%d_%H%M%S')}.wav"

    # Ensure the directory exists (create if it doesn't)
    os.makedirs(directory, exist_ok=True)
    
    # Construct the file path (you might want to name the file dynamically)
    file_path = os.path.join(directory, filename)
    
    # Stream the response to the file
    response.stream_to_file(file_path)

    return file_path

def query_chatgpt2(**kwargs):
    """
    Gives more information if the user wants to know more about a specific 
    celestial body. The function only executes if the variable know_more is True.
    """ 
    client = OpenAI(api_key=OPENAI_KEY)
    user_ans = kwargs["user_answer"]
    previous_txt = kwargs["previous_ans"]

    completion = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", 
        "content": "You are an astrophysics expert named Nova who answers users inquiries about \
                    the space and celestial bodies. You previously answered a question \
                    from the user, know he may want to know more about the celestial body. \
                    If he answered with YES or something similar, provide more information \
                    about the body, first telling him you are glad about his interest. \
                    If he said NO or something similar, thank him and ask him if he \
                    needs help with anything else. Always keep answers short. No more than \
                    two sentences."},
        {"role": "user", "content": f"You previously said: {previous_txt}. Now, this is my response {user_ans}."}
    ]
    )

    message = completion.choices[0].message.content
    

    print(f"\n\n{message}\n\n")

    return message


