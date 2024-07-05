from pathlib import Path
from openai import OpenAI
from dotenv import load_dotenv 
load_dotenv()


client = OpenAI()

file_path = "output/speaker_SPEAKER_00/interview-10001.wav"

audio_file= open(file_path, "rb")
transcript = client.audio.transcriptions.create(
  model="whisper-1",
  response_format="text", # Default output format is json,if want in json format, just comment out response format
  file=audio_file
)
print(transcript)