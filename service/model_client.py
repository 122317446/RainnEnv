# ==========================================
# File: model_client.py
# Created in iteration: 3
# Author: Karl Concha
#
# Notes:
# Provides a simple abstraction layer for AI model calls.
# AgentRuntime should depend on this interface rather than any specific backend.
# ==========================================

class ModelClient:
    """ Base interface for model clients. """

    def generate(self, model_name, prompt):
        """ Returns a generated string response for a given prompt. """
        raise NotImplementedError("ModelClient.generate() must be implemented by a subclass.")


class MockModelClient(ModelClient):
    """
    Mock client used for testing the Stage Execution Engine.
    This avoids dependency on any external model during development.
    """

    def generate(self, model_name, prompt):
        # Keep it simple but deterministic enough to see stage chaining work
        return (
            f"[MOCK MODEL OUTPUT]\n"
            f"model={model_name}\n"
            f"prompt_chars={len(prompt)}\n"
            f"prompt_preview={prompt[:200]}\n"
        )
