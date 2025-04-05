import os
import yaml
from ollama import chat  # import ollama chat function

class OllamaModel:
    def __init__(self, model: str):
        self.model = model  # e.g. "qwen2.5-coder:14b-instruct-q4_K_M"

    def __call__(self, prompt: str, stop_sequences=None):
        messages = [{"role": "user", "content": prompt}]
        # For simplicity, we do a synchronous call here:
        response = chat(model=self.model, messages=messages)
        return response.message.content

class OllamaEmbedding:
    def __init__(self, model: str):
        self.model = model

    def embed(self, text: str):
        # Call the Ollama embed endpoint (this is a simplified example)
        # Assuming the ollama library has an 'embed' function:
        from ollama import embed
        response = embed(model=self.model, input=text)
        return response["embeddings"]

class AIModel:
    def __init__(self):
        # Read configuration from config.yaml; if not found, use defaults.
        if os.path.exists("config.yaml"):
            with open("config.yaml", "r") as f:
                config = yaml.safe_load(f)
        else:
            config = {
                "agent_model": "qwen2.5-coder:14b-instruct-q4_K_M",
                "embedding_model": "bge-m3:latest",
                "manager_model": "llama3.2"
            }
        self.agent_model_name = config.get("agent_model")
        self.embedding_model_name = config.get("embedding_model")
        self.manager_model_name = config.get("manager_model")
        # Use OllamaModel for generating completions
        self.model = OllamaModel(model=self.agent_model_name)
        self.embedding = OllamaEmbedding(model=self.embedding_model_name)
        # In a full implementation you might also instantiate a manager AI model

    def analyze_code(self, code: str) -> str:
        prompt = (
            "Analyze the following Python code for potential improvements and "
            "identify any bugs:\n\n" + code
        )
        return self.model(prompt, stop_sequences=["<end>"])

    def refactor_code(self, code: str) -> str:
        prompt = (
            "Provide refactoring suggestions for the following Python code. "
            "Include variable renaming, improved readability, and potential bug fixes:\n\n" + code
        )
        return self.model(prompt, stop_sequences=["<end>"])

    def get_embedding(self, text: str):
        return self.embedding.embed(text)
