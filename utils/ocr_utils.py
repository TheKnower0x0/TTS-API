import os
import torch
from PIL import Image
from transformers import Qwen2VLForConditionalGeneration, AutoProcessor
from peft import PeftModel


class OCR:
    """
    A class for Optical Character Recognition (OCR) using Tesseract.
    """
    prompt: str = (
        "Below is the image of one page of a document, as well as some raw textual content that was previously "
        "extracted for it. Just return the plain text representation of this document as if you were reading it "
        "naturally. Do not hallucinate.")

    model_name: str
    max_tokens: int
    model = None
    processor = None

    def __init__(self, model_name: str = "NAMAA-Space/Qari-OCR-0.1-VL-2B-Instruct",
                 adapter: str = "unsloth/qwen2-vl-2b-instruct-unsloth-bnb-4bit", max_tokens: int = 2000):
        """
        Initialize the OCR class with the path to the Tesseract executable.

        Args:
            model_name (str): The name of the pre-trained model.
            adapter (str): The name of the adapter model.
            max_tokens (int): The maximum number of tokens to generate.
        """
        self.model_name = model_name
        self.max_tokens = max_tokens
        self.model = Qwen2VLForConditionalGeneration.from_pretrained(
            model_name,
            torch_dtype=torch.float16,
            device_map="auto",
            trust_remote_code=True,
        )
        self.model = PeftModel.from_pretrained(self.model, adapter, torch_dtype="torch.float16")

        self.processor = AutoProcessor.from_pretrained(model_name, use_fast=True)

    def extract_text(self, image: Image.Image) -> str:
        """
        Extract text from an image using Tesseract OCR.

        Args:
            image (Image.Image): The image to extract text from.

        Returns:
            str: The extracted text.
        """

        # Save the image to a temporary file
        src: str = "temp_image.png"
        image.save(src)
        message = [
            {
                "role": "user",
                "content": [
                    {"type": "image", "image": f"file://{src}"},
                    {"type": "text", "text": self.prompt},
                ],
            }
        ]
        text = self.processor.apply_chat_template(message, tokenize=False, add_generation_prompt=True)

        device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"Using device: {device}")

        inputs = self.processor(text=[text], images=[image], padding=True, return_tensors="pt").to(self.model.device)

        generated_ids = self.model.generate(**inputs, max_new_tokens=self.max_tokens)

        generated_ids_trimmed = [
            out_ids[len(in_ids):] for in_ids, out_ids in zip(inputs.input_ids, generated_ids)
        ]

        extracted_text = self.processor.batch_decode(
            generated_ids_trimmed, skip_special_tokens=True, clean_up_tokenization_spaces=False
        )[0]

        # Clean up the temporary file
        os.remove(src)

        return extracted_text
