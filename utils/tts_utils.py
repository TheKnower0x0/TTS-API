import tempfile
from elevenlabs.client import ElevenLabs


class TTS:
    """
    A class for Text-to-Speech (TTS) using the ElevenLabs API.
    """

    voices = {
        "Aisha": "21m00Tcm4TlvDq8ikWAM",
        "Rashid": "29vD33N1CtxCmqQRPOHJ",
        "Zain": "2EiwWnXFnvU5JabPnv8n",
        "Ali": "5Q0t7uMcjvnagumLfvZi",
        "Khadija": "9BWtsMINqrJLrRacOk9x",
        "Najwa": "AZnzlk1XvdvUeBnXmlld",
        "Zaydoun": "CYw3kZ02Hs0563khs1Fj",
        "Adam": "CwhRBWXzGAHq8TQ4Fs17",
        "Yassin": "D38z5RcWu1voky8WS1ja",
        "Shahrazad": "EXAVITQu4vr4xnSDxMaL"
    }

    def __init__(self, api_key: str):
        """
        Initialize the TTS class with the ElevenLabs API key.

        Args:
            api_key (str): The API key for ElevenLabs.
        """
        if not api_key:
            raise ValueError("API key is required for ElevenLabs.")
        self.client = ElevenLabs(api_key=api_key)

    def text_to_speech(self, text: str, voice: str = "Aisha") -> str:
        """
        Convert text to speech using ElevenLabs API and save the audio file.

        Args:
            text (str): The text to convert to speech.
            voice (str): The name of the voice to use for TTS.

        Returns:
            str: Path to the generated audio file.
        """
        if voice not in self.voices:
            raise ValueError(f"Voice '{voice}' is not supported. Available voices: {', '.join(self.voices.keys())}")

        voice_id = self.voices[voice]

        try:
            audio_generator = self.client.text_to_speech.convert(
                text=text,
                voice_id=voice_id,
                model_id="eleven_multilingual_v2",
                output_format="mp3_44100_128"
            )
            audio_bytes = b"".join(audio_generator)
        except Exception as e:
            raise RuntimeError(f"Failed to generate speech: {e}")

        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_file:
            temp_file.write(audio_bytes)
            return temp_file.name
