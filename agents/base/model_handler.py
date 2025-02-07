from huggingface_hub import InferenceClient
import os

class AIModelHandler:
    def __init__(self):
        self.client = InferenceClient(
            model="codellama/CodeLlama-7b-hf",
            token=os.getenv("HUGGINGFACEHUB_API_TOKEN")
        )
    
    def query_model(self, prompt, max_new_tokens=100):
        return self.client.text_generation(prompt, max_new_tokens=max_new_tokens)