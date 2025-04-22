from PIL import Image
import pytesseract


def extract_arabic_text(image: Image.Image, lang: str) -> str:
    """
    Extract Arabic text from an image using Tesseract OCR.

    Args:
        image (Image.Image): The input image.
        lang (str): The language code for OCR (e.g., 'ara' for Arabic).

    Returns:
        str: The extracted text.
    """
    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    return pytesseract.image_to_string(image, lang=lang).strip()
