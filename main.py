from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from PIL import Image
from utils.ocr_utils import extract_arabic_text
from utils.language_utils import LanguageModelUtils
from utils.tts_utils import text_to_speech_arabic
import io


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Perform startup tasks
    print("Application startup...")
    yield
    # Perform shutdown tasks
    print("Application shutdown...")


# Initialize FastAPI application
app = FastAPI(lifespan=lifespan)

# Enable Cross-Origin Resource Sharing (CORS) for all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

# Load the language model once at application startup
model_name = "unsloth/Llama-3.2-1B-bnb-4bit"
language_model_utils = LanguageModelUtils(model_name=model_name)


# Endpoint to check the health of the API
@app.get("/")
async def health_check():
    """
    Health check endpoint to verify if the API is running.

    Returns:
        JSONResponse: A simple message indicating the API is running.
    """
    return JSONResponse({"message": "API is running"})


# Endpoint to extract Arabic text from an uploaded image
@app.post("/ocr")
async def extract_text(file: UploadFile = File(...), lang: str = Form("ara")):
    """
    Extract Arabic text from an uploaded image.

    Args:
        file (UploadFile): The image file to process.
        lang (str): The language code for OCR (default is 'ara').

    Returns:
        JSONResponse: Extracted text or an error message.
    """
    try:
        image_bytes = await file.read()
        image = Image.open(io.BytesIO(image_bytes))
        arabic_text = extract_arabic_text(image, lang=lang)
        return JSONResponse({"extracted_text": arabic_text})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)


# Endpoint to generate a response using the LLaMA language model
@app.post("/respond")
async def generate_response(text: str = Form(...)):
    """
    Generate a response from the LLaMA language model.

    Args:
        text (str): The input text for the model.

    Returns:
        JSONResponse: Generated response or an error message.
    """
    try:
        result = language_model_utils.generate_response(text)
        return JSONResponse(result)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)


# Endpoint to convert text to speech and return an audio file
@app.post("/tts")
async def text_to_speech(text: str = Form(...), lang: str = Form("ar")):
    """
    Convert text to speech and return the audio file.

    Args:
        text (str): The text to convert to speech.
        lang (str): The language code for TTS (default is 'ar').

    Returns:
        FileResponse: The generated audio file or an error message.
    """
    try:
        audio_file_path = text_to_speech_arabic(text, lang=lang)
        return FileResponse(audio_file_path, media_type="audio/mpeg", filename="output.mp3")
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
