import unsloth
from unsloth import FastLanguageModel
from transformers import AutoTokenizer
import time


class LanguageModel:
    """
    Utility class for interacting with the LLaMA language model.
    """

    def __init__(self, model_name: str, max_seq_length: int = 5020):
        """
        Initialize the language model and tokenizer.

        Args:
            model_name (str): The name of the pre-trained model.
            max_seq_length (int): The maximum sequence length for inputs.
        """
        self.tokenizer = AutoTokenizer.from_pretrained(model_name, use_fast=True)
        model, tokenizer = FastLanguageModel.from_pretrained(
            model_name=model_name,
            max_seq_length=max_seq_length,
            load_in_4bit=True,
            dtype=None,
        )
        self.model = FastLanguageModel.for_inference(model)

    def generate_response(self, text: str, max_length: int = 500) -> dict:
        """
        Generate a response from the language model.

        Args:
            text (str): The input text.
            max_length (int): The maximum length of the generated response.

        Returns:
            dict: The generated response or an error message.
        """
        try:
            inputs = self.tokenizer(text, return_tensors="pt", padding=True, truncation=True)
            inputs = inputs.to(self.model.device)

            start_time = time.time()
            outputs = self.model.generate(inputs['input_ids'], max_length=max_length)
            end_time = time.time()

            response_text = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            elapsed_time = round(end_time - start_time, 4)

            return {
                "response": response_text.strip(),
                "inference_time_seconds": elapsed_time
            }
        except Exception as e:
            return {"error": str(e)}
