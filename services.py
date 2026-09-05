import time
from typing import Generator
from google.genai import types
from google.genai.errors import APIError

from .config import gemini_client, MODEL_NAME
from .models import LogAnalysisSchema 

SYSTEM_INSTRUCTION = (
        "You are an expert .NET and Cloud Architecture AI Engineer. "
        "Analyze the provided log file. Identify the root cause, pinpoint the "
        "exact line of failure if available, and provide a concrete production-ready C# fix."
    )

def get_token_count(prompt: str) -> int:
    """Calculates the token payload size for the request."""
    response = gemini_client.models.count_tokens(
        model=MODEL_NAME,
        contents=prompt,
        config=types.CountTokensConfig()
    )
    return response.total_tokens

def analyze_log_stream(
    log_content: str, 
    retries: int = 3, 
    initial_delay: int = 5
) -> Generator[str, None, None]:
    """
    Sends log data to Gemini and yields raw JSON text chunks as they arrive.
    Implements exponential backoff on 503 errors.
    """
    prompt = f"Please analyze this .NET log:\n\n{log_content}"
    delay = initial_delay

    for attempt in range(retries):
        try:
            response = gemini_client.models.generate_content_stream(
                model=MODEL_NAME,
                contents=prompt,
                config=types.GenerateContentConfig(
                    system_instruction=SYSTEM_INSTRUCTION,
                    temperature=0.2,
                    response_mime_type="application/json",
                    response_schema=LogAnalysisSchema
                )
            )
            
            for chunk in response:
                if chunk.text:
                    yield chunk.text
            return  # Successful execution completes the generator

        except APIError as e:
            # Handle server overloads (503) with exponential backoff
            if e.code == 503 and attempt < retries - 1:
                time.sleep(delay)
                delay *= 2
            else:
                raise e