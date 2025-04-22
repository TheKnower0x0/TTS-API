# TTS-API

## Overview
This project provides a FastAPI-based backend for performing the following tasks:
1. **OCR (Optical Character Recognition)**: Extract Arabic text from images.
2. **Language Model Response Generation**: Generate responses using the LLaMA language model.
3. **Text-to-Speech (TTS)**: Convert text to speech and return an audio file.

## Endpoints

### 1. `/ocr` - Extract Arabic Text from Images
- **Method**: `POST`
- **Description**: Upload an image to extract Arabic text using OCR.
- **Request**:
  - `file` (form-data): The image file.
  - `lang` (form-data, optional): Language code (default: `ara`).
- **Response**:
  - Extracted text in JSON format.

### 2. `/respond` - Generate Response from LLaMA
- **Method**: `POST`
- **Description**: Generate a response using the LLaMA language model.
- **Request**:
  - `text` (form-data): Input text for the model.
- **Response**:
  - Generated response in JSON format.

### 3. `/tts` - Convert Text to Speech
- **Method**: `POST`
- **Description**: Convert text to speech and return an audio file.
- **Request**:
  - `text` (form-data): Text to convert to speech.
  - `lang` (form-data, optional): Language code (default: `ar`).
- **Response**:
  - Audio file in MP3 format.

## How to Use with Frontend
1. **OCR**:
   - Use a file input to upload an image.
   - Send a `POST` request to `/ocr` with the image file and optional language code.
   - Display the extracted text from the response.

2. **Response Generation**:
   - Send a `POST` request to `/respond` with the input text.
   - Display the generated response from the API.

3. **Text-to-Speech**:
   - Send a `POST` request to `/tts` with the text and optional language code.
   - Play or download the returned MP3 file.

## Setup
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the FastAPI server:
   ```bash
   uvicorn main:app --reload
   ```   
3. Access the API documentation at `http://localhost:8000/docs` to test the endpoints interactively.   
   
# Prerequisites

## Install CUDA
Ensure that CUDA is installed on your computer to enable GPU acceleration for supported libraries.

- Download CUDA from the [NVIDIA CUDA Toolkit website](https://developer.nvidia.com/cuda-toolkit).
- Follow the installation instructions for your operating system.

## Install Tesseract OCR
- Download and install Tesseract OCR from the [Tesseract GitHub Releases](https://github.com/tesseract-ocr/tesseract).
- During installation, ensure you select the option to add Tesseract to your system's PATH.

## Set the TESSDATA_PREFIX Environment Variable

### On Windows:
1. Open the Start menu and search for "Environment Variables".
2. Click on "Edit the system environment variables".
3. Under "System Properties", click "Environment Variables".
4. Add a new system variable:
   - **Variable Name**: `TESSDATA_PREFIX`
   - **Variable Value**: `C:\Program Files\Tesseract-OCR\tessdata` (or the path to your tessdata folder)

### On Linux/Mac:
Add the following line to your shell configuration file (e.g., `.bashrc` or `.zshrc`):

```bash
export TESSDATA_PREFIX=/usr/share/tesseract-ocr/4.00/tessdata
```