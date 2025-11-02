from google.cloud import speech
from google.cloud import texttospeech
import os,time


os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "warm-canto-453503-u3-e67ff607230a.json"


def synthesize_text(text, output_file=None, language_code="th-TH", 
                    voice_name="th-TH-Chirp3-HD-Autonoe", speaking_rate=1.25,):
    """
    Synthesizes speech from the input text.
    
    Args:
        text: The text to synthesize.
        output_file: The name of the output audio file.
        language_code: The language code.
        voice_name: The voice name.
        speaking_rate: The speaking rate (1.0 is normal speed).
        pitch: The pitch of the voice (0.0 is normal pitch).
    """

    if output_file is None:
        output_file = f"output_{int(time.time())}.mp3"
    client = texttospeech.TextToSpeechClient()

    synthesis_input = texttospeech.SynthesisInput(text=text)

    voice = texttospeech.VoiceSelectionParams(
        language_code=language_code,
        name=voice_name
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3,
        speaking_rate=speaking_rate,
    )

    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    with open(output_file, "wb") as out:
        out.write(response.audio_content)
        print(f'Audio content written to "{output_file}"')

    return output_file

if __name__ == "__main__":
    synthesize_text('สวัสดีค่ะ')