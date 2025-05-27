# app/models/gemini_model.py

import google.generativeai as genai
import os

class GeminiChatModel:
    def __init__(self, model_name="gemini-pro", api_key=None):
        self.model_name = model_name
        self.api_key = api_key or os.getenv("GOOGLE_API_KEY")
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel(model_name)

    async def run(self, messages: list[dict]):
        """
        Mimics OpenAI ChatCompletion API using Gemini
        Expects messages as: [{"role": "user", "content": "hello"}]
        """
        prompt = self._format_messages(messages)
        response = self.model.generate_content(prompt)
        return response.text

    def _format_messages(self, messages):
        # Combine messages into a single prompt (simple linear history)
        return "\n".join([f"{m['role']}: {m['content']}" for m in messages])
