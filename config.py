import os
from dotenv import load_dotenv
from google.genai import Client

# Load environment variables
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("Missing GEMINI_API_KEY in the environment or .env file")

# Single source of truth for the client and settings
gemini_client = Client(api_key=GEMINI_API_KEY)
MODEL_NAME = "gemini-3.6-flash"
