import requests

class OllamaModelClient:

    def __init__(self, host="http://localhost:11434"):
        self.host = host

    def generate(self, model_name, prompt):
        r = requests.post(f"{self.host}/api/generate",
                          json={"model": model_name, 
                                "prompt": prompt,
                                "stream": False},
                                timeout=120)
        
        r.raise_for_status() #Learn what this does
        data = r.json()
        return(data.get("response") or "").strip()