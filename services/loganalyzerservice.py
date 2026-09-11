from pydantic import ValidationError

from core.llmclient import LLMClient
from models import LogAnalysisSchema


class LogAnalyzerService:
    def __init__(self, llm_client: LLMClient):
        self.llm_client = llm_client

    def analyze_log_file(self, logfile: str) -> LogAnalysisSchema:
        try:
            with open(logfile, "r", encoding="utf-8") as file:
                log_content = file.read()
        except FileNotFoundError as exc:
            raise FileNotFoundError(
                f"The file '{logfile}' was not found.") from exc

        prompt = f"Please analyze this .NET log:\n\n{log_content}"
        tokens = self.llm_client.get_token_count(prompt)
        print("📊 Token Optimization Info:")
        print(f"   - Input payload size: {tokens} tokens.")
        print("   - Gemini Context Window Limit: 1,048,576 tokens.\n")

        raw_json = ""

        try:
            for chunk in self.llm_client.analyze_log_stream(log_content):
                raw_json += chunk
        except Exception as exc:
            raise RuntimeError(f"Analysis failed: {exc}") from exc

        if not raw_json.strip():
            raise ValueError("The LLM returned an empty response.")

        try:
            parsed = LogAnalysisSchema.model_validate_json(raw_json)
        except ValidationError as exc:
            raise ValueError(
                f"LLM response failed schema validation: {exc}") from exc

        print("\n\n=================================")
        print("✅ Stream complete. Output conforms to the JSON schema.")
        return raw_json
