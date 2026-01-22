# ==========================================
# File: model_client_ollama.py
# Created in iteration: 3
# Author: Karl Concha
#
# Lightweight client for calling a locally hosted Ollama instance.
#
# Notes:
# - Uses the /api/generate endpoint with stream=False
# - Raises exceptions for HTTP/network errors so the runtime can mark stages FAILED
#
# #ChatGPT (OpenAI, 2025) – Assisted in structuring a minimal Ollama model
# client abstraction with explicit error propagation to support safe
# stop-on-failure behaviour during stage execution.
# Conversation Topic: "Integrating Ollama into Rainn"
# Date: January 2026
#
# Used by StageExecutionEngine to generate stage output within agent_runtime_service
# ==========================================

import requests


class OllamaModelClient:
    """
    Minimal Ollama HTTP client for localhost.
    """

    def __init__(self, host="http://localhost:11434", timeout_seconds=120):
        self.host = host.rstrip("/")
        self.timeout_seconds = timeout_seconds

    def generate(self, model_name, prompt):
        """
        Generate a single response from Ollama (non-streaming) with needed parameters given.
        """

        payload = {
            "model": model_name,
            "prompt": prompt,
            "stream": False
        } #The packet of data to send to ollama 

        r = requests.post(
            f"{self.host}/api/generate",
            json=payload, #specifying the payload to be json
            timeout=self.timeout_seconds
        )

        # If Ollama returns 4xx/5xx this will raise, and the runtime will mark stage FAILED.
        r.raise_for_status()

        data = r.json() if r.content else {} #converting JSON into a readable python object
        response_text = (data.get("response") or "").strip() #response within the object is only collected

        if not response_text:
            # Keep this explicit: an empty response is treated as a failed stage.
            raise Exception("Ollama returned an empty response.")

        return response_text
