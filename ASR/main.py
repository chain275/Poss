from Recorder import SentenceRecorder
from Asr import transcribe_audio_file
import time
from openai import OpenAI
api = ''
client = OpenAI(api_key=api,base_url="https://api.opentyphoon.ai/v1")

recorder = SentenceRecorder(silence_threshold=1000,pause_duration=1.75,sample_rate=44100,output_dir="recordings")
while True:
    transcription = transcribe_audio_file(recorder.record_continuously(),client=client)
    if transcription.text.strip() != '':
        print(f"Transcription: {transcription.text}")