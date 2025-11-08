import requests
from base_provider import BaseProvider
from config import OLLAMA_MODEL, OLLAMA_URL

class OllamaProvider(BaseProvider):
    def __init__(self):
        self.model = OLLAMA_MODEL
        self.url = OLLAMA_URL

    def generate(self, prompt: str) -> str:
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False
        }
        try:
            response = requests.post(self.url, json=payload, timeout=120)
            response.raise_for_status()
            data = response.json()
            return data.get("response", "").strip()
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"Ollama connection error: {e}")
        except Exception as e:
            raise RuntimeError(f"Unexpected error: {e}")
