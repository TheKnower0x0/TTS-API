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