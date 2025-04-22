from gtts import gTTS
import tempfile


def text_to_speech_arabic(text: str, lang: str = 'ar') -> str:
    """
    Convert text to speech and save it as an audio file.

    Args:
        text (str): The text to convert to speech.
        lang (str): The language code for TTS (default is 'ar').

    Returns:
        str: The path to the generated audio file.
    """
    tts = gTTS(text, lang=lang)
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
    tts.save(temp_file.name)
    return temp_file.name
