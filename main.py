from subprocess import CalledProcessError, run
from pyannote.audio import Pipeline
import os

hf_token = os.environ["HUGGINGFACE_TOKEN"]
def split_audio(input_file, output_file, start, end):
    length = end - start
    cmd = ["ffmpeg", "-ss", str(start), "-i", input_file, "-t", str(length), "-vn", "-acodec", "pcm_s16le", "-ar", "48000", "-ac", "1", output_file]
    try:
        run(cmd, capture_output=True, check=True).stdout
    except CalledProcessError as e:
        raise RuntimeError(f"FFMPEG error {str(e)}")
        
pipeline = Pipeline.from_pretrained(
    "pyannote/speaker-diarization@2.1",
    use_auth_token= hf_token
)



input_wav = "podcast.wav"
output_dir = "output"
count = 10001

# inference
diarization = pipeline(input_wav)

if not os.path.isdir(output_dir):
    os.makedirs(output_dir)

for turn, _, speaker in diarization.itertracks(yield_label=True):
    print(f"start={turn.start}s stop={turn.end}s speaker_{speaker}")

    speaker_dir = f"{output_dir}/speaker_{speaker}/"
    if not os.path.isdir(speaker_dir):
        os.mkdir(speaker_dir)

    filename = os.path.join(speaker_dir, f"interview-{count}.wav")
    split_audio(input_wav, filename, turn.start, turn.end)
    count += 1



