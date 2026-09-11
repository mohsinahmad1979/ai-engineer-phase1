import time
from typing import Generator

from google.genai import Client, types
from google.genai.errors import APIError

from config import GEMINI_API_KEY
from core.llmclient import LLMClient
from models import LogAnalysisSchema

SYSTEM_INSTRUCTION = (
    "You are an expert .NET and Cloud Architecture AI Engineer. "
    "Analyze the provided log file. Identify the root cause, pinpoint the "
    "exact line of failure if available, and provide a concrete "
    "production-ready C# fix."
)


class GeminiLLMClient(LLMClient):
    def __init__(self, api_key: str | None = None, model_name: str = "gemini-3.6-flash"):
        self.api_key = api_key or GEMINI_API_KEY
        self.gemini_client = Client(api_key=self.api_key)
        self.MODEL_NAME = model_name

    def get_token_count(self, prompt: str) -> int:
        """Calculates the token payload size for the request."""
        response = self.gemini_client.models.count_tokens(
            model=self.MODEL_NAME,
            contents=prompt,
            config=types.CountTokensConfig(),
        )
        return int(response.total_tokens)

    def analyze_log_stream(
        self,
        log_content: str,
        retries: int = 3,
        initial_delay: int = 5,
    ) -> Generator[str, None, None]:
        """
        Sends log data to Gemini and yields raw JSON text chunks as they arrive.
        Implements exponential backoff on 503 errors.
        """
        prompt = f"Please analyze this .NET log:\n\n{log_content}"
        delay = initial_delay

        schema_dict = LogAnalysisSchema.model_json_schema()
        schema_dict.pop("additionalProperties", None)

        for attempt in range(retries):
            try:
                response = self.gemini_client.models.generate_content_stream(
                    model=self.MODEL_NAME,
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        system_instruction=SYSTEM_INSTRUCTION,
                        temperature=0.2,
                        response_mime_type="application/json",
                        response_schema=schema_dict,
                    ),
                )

                for chunk in response:
                    text = getattr(chunk, "text", None)
                    if text:
                        yield text

                return

            except APIError as e:
                if e.code == 503 and attempt < retries - 1:
                    time.sleep(delay)
                    delay *= 2
                    continue
                raise
