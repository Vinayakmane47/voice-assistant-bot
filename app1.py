import os
import ffmpeg
from pydub import AudioSegment
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
api_key = os.getenv('OPENAI_API_KEY')

# Initialize OpenAI client
client = OpenAI(api_key=api_key)

# Define the text for each speaker
text_speaker_1 = "Your time is limited, so don’t waste it living someone else’s life. Don’t be trapped by dogma — which is living with the results of other people’s thinking."
text_speaker_2 = "Don’t let the noise of others’ opinions drown out your own inner voice. And most important, have the courage to follow your heart and intuition. They somehow already know what you truly want to become. Everything else is secondary...Stay Hungry. Stay Foolish."

# Generate speech for each speaker
response_speaker_1 = client.audio.speech.create(
    model="tts-1-hd",
    voice="echo",
    input="Interviewer: Can you share some advice for our listeners about making the most of their time?  " 
)

response_speaker_2 = client.audio.speech.create(
    model="tts-1-hd",
    voice="nova",
    input="Interviewer: That's a great point. How can we stay true to ourselves in the face of external pressures?  " 
)

# Save the audio files
audio_file_path_1 = "speaker_1.ogg"
audio_file_path_2 = "speaker_2.ogg"

with open(audio_file_path_1, "wb") as f:
    f.write(response_speaker_1.content)

with open(audio_file_path_2, "wb") as f:
    f.write(response_speaker_2.content)

# Convert the audio files to WAV format using ffmpeg
wav_file_path_1 = "speaker_1.wav"
wav_file_path_2 = "speaker_2.wav"

ffmpeg.input(audio_file_path_1).output(wav_file_path_1).run()
ffmpeg.input(audio_file_path_2).output(wav_file_path_2).run()

# Combine the audio files using pydub
audio1 = AudioSegment.from_wav(wav_file_path_1)
audio2 = AudioSegment.from_wav(wav_file_path_2)

combined_audio = audio1 + AudioSegment.silent(duration=500) + audio2

# Export the combined audio to a file
combined_audio.export("podcast.wav", format="wav")

print("Podcast audio saved as podcast.wav")
