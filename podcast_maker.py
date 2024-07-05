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
text_speaker_1 = "The environment is a pressing issue that requires immediate attention. We need to reduce carbon emissions and invest in renewable energy."
text_speaker_2 = "While renewable energy is important, we also need to focus on conserving natural habitats and protecting wildlife from the effects of climate change."
text_speaker_3 = "I agree with both points, but we must also consider the economic impact of environmental policies. We need solutions that balance ecological preservation with economic growth."

# Generate speech for each speaker
response_speaker_1 = client.audio.speech.create(
    model="tts-1-hd",
    voice="echo",
    input=text_speaker_1
)

response_speaker_2 = client.audio.speech.create(
    model="tts-1-hd",
    voice="nova",
    input=text_speaker_2
)

response_speaker_3 = client.audio.speech.create(
    model="tts-1-hd",
    voice="shimmer",
    input=text_speaker_3
)

# Create directories if they don't exist
os.makedirs("speaker/ogg", exist_ok=True)
os.makedirs("speaker/wav", exist_ok=True)
os.makedirs("podcast", exist_ok=True)

# Save the audio files in the 'speaker' folder
audio_file_path_1 = "speaker/ogg/speaker_1.ogg"
audio_file_path_2 = "speaker/ogg/speaker_2.ogg"
audio_file_path_3 = "speaker/ogg/speaker_3.ogg"

with open(audio_file_path_1, "wb") as f:
    f.write(response_speaker_1.content)

with open(audio_file_path_2, "wb") as f:
    f.write(response_speaker_2.content)

with open(audio_file_path_3, "wb") as f:
    f.write(response_speaker_3.content)

# Convert the audio files to WAV format using ffmpeg
wav_file_path_1 = "speaker/wav/speaker_1.wav"
wav_file_path_2 = "speaker/wav/speaker_2.wav"
wav_file_path_3 = "speaker/wav/speaker_3.wav"

ffmpeg.input(audio_file_path_1).output(wav_file_path_1).run()
ffmpeg.input(audio_file_path_2).output(wav_file_path_2).run()
ffmpeg.input(audio_file_path_3).output(wav_file_path_3).run()

# Combine the audio files using pydub
audio1 = AudioSegment.from_wav(wav_file_path_1)
audio2 = AudioSegment.from_wav(wav_file_path_2)
audio3 = AudioSegment.from_wav(wav_file_path_3)

combined_audio = audio1 + AudioSegment.silent(duration=500) + audio2 + AudioSegment.silent(duration=500) + audio3

# Export the combined audio to a file
combined_audio.export("podcast/environment_debate.wav", format="wav")

print("Podcast audio saved as environment_debate.wav")
