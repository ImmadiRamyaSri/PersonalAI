import os
from groq import Groq  
from dotenv import load_dotenv

load_dotenv()
client = Groq()

def transcribe_audio(file_path):
    if not os.path.exists(file_path):
        return None
    
    with open(file_path,'rb') as audio_file:
           transcription = client.audio.transcriptions.create(
                       model = "whisper-large-v3",
                       file = audio_file
           )
    return transcription.text