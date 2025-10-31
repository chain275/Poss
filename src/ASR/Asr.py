def transcribe_audio_file(audio_file_path,client):
    try:
        with open(audio_file_path, 'rb') as audio_file:
            transcription = client.audio.transcriptions.create(
                file=audio_file,
                model="typhoon-asr-realtime"
            )
            return transcription
    except Exception as e:
        print(f"Error transcribing audio: {e}")
        return None