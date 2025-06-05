import io
import os
from contextlib import asynccontextmanager

from PIL import Image
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse

from utils.ocr_utils import OCR
from utils.tts_utils import TTS
from dotenv import load_dotenv


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

# Load environment variables
load_dotenv()

# Load Models
print("Loading models...")
ocr = OCR(model_name=os.getenv("BASE_OCR_MODEL"), adapter=os.getenv("ADAPTER_OCR_MODEL"),
          max_tokens=int(os.getenv("MAX_TOKENS")))

tts = TTS(api_key=os.getenv("ELEVENLABS_API_KEY"))
print("Models loaded successfully.")


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
async def extract_text(file: UploadFile = File(...)):
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
        extracted_text = ocr.extract_text(image)
        return JSONResponse({"extracted_text": extracted_text})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)


# Endpoint to convert text to speech and return an audio file
@app.post("/tts")
async def text_to_speech(text: str = Form(...), voice: str = Form("Aisha")):
    """
    Convert text to speech and return the audio file.

    Args:
        text (str): The text to convert to speech.
        voice (str): The language code for TTS (default is 'ar').

    Returns:
        FileResponse: The generated audio file or an error message.
    """
    try:
        audio_file_path = tts.text_to_speech(text=text, voice=voice)
        return FileResponse(audio_file_path, media_type="audio/mpeg", filename="output.mp3")
    except Exception as e:
        print(f"Error in TTS: {e}")
        return JSONResponse(content={"error": str(e)}, status_code=500)
