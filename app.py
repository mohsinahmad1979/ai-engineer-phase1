import os
from dotenv import load_dotenv
# Change these two lines to import Client explicitly
from google.genai import Client
from google.genai import types
import time
from google.genai.errors import ServerError


# Load API Key from .env file
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("Missing GEMINI_API_KEY in .env file")

# Use the explicitly imported Client class here (Capital 'C')
client = Client(api_key=api_key)


def analyze_log_with_retry(log_file_path, retries=3, delay=5):
    with open(log_file_path, 'r') as file:
        log_content = file.read()
        
    system_instruction = (
        "You are an expert .NET and Cloud Architecture AI Engineer. "
        "Analyze the provided log file. Identify the root cause, pinpoint the "
        "exact line of failure if available, and provide a concrete production-ready C# fix."
    )

    for attempt in range(retries):
        try:
            print(f"⏳ Sending log data to Gemini (Attempt {attempt + 1}/{retries})...")
            response = client.models.generate_content(
                model='gemini-3.6-flash',
                contents=f"Please analyze this .NET log:\n\n{log_content}",
                config=types.GenerateContentConfig(
                    system_instruction=system_instruction,
                    temperature=0.2,
                )
            )
            return response.text
        except ServerError as e:
            if e.code == 503 and attempt < retries - 1:
                print(f"⚠️ Server overloaded (503). Retrying in {delay} seconds...")
                time.sleep(delay)
                delay *= 2  # Exponential backoff
            else:
                raise e
        

if __name__ == "__main__":
    log_path = "sample.log"
    analyses_result = analyze_log_with_retry(log_path)
    print("\n Analyses result is as follows:\n"
          )
    print(analyses_result)
