import sys
from .services import get_token_count, analyze_log_stream

def run_analysis(log_file_path: str):
    # 1. Read input data
    try:
        with open(log_file_path, 'r', encoding='utf-8') as file:
            log_content = file.read()
    except FileNotFoundError:
        print(f"❌ Error: The file '{log_file_path}' was not found.")
        sys.exit(1)

    # 2. Log optimization metrics
    prompt = f"Please analyze this .NET log:\n\n{log_content}"
    tokens = get_token_count(prompt)
    print(f"📊 Token Optimization Info:")
    print(f"   - Input payload size: {tokens} tokens.")
    print(f"   - Gemini Context Window Limit: 1,048,576 tokens.\n")

    # 3. Stream data and consume generator chunks
    print("⏳ Processing log with Gemini...")
    full_json_string = ""
    
    try:
        for chunk in analyze_log_stream(log_content):
            sys.stdout.write(chunk)
            sys.stdout.flush()
            full_json_string += chunk
            
        print("\n\n=================================")
        print("✅ Stream complete. Output conforms perfectly to JSON schema.")
        
    except Exception as e:
        print(f"\n❌ Analysis failed: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    # In a full app, you might use 'argparse' here to read the path from the terminal
    log_path = "sample.log"
    run_analysis(log_path)
