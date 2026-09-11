import argparse

from clients.geminillmclient import GeminiLLMClient
from services.loganalyzerservice import LogAnalyzerService


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Analyze .NET log files with Gemini.")
    parser.add_argument(
        "logfile",
        nargs="?",
        default="sample.log",
        help="Path to the .NET log file to analyze.",
    )
    args = parser.parse_args()

    client = GeminiLLMClient()
    service = LogAnalyzerService(client)
    print(service.analyze_log_file(args.logfile))


if __name__ == "__main__":
    main()
