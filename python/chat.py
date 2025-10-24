#!/usr/bin/env python3
from ollama import Client
import os
import sys

# Windows上のOllamaに接続（環境変数から取得）
ollama_host = os.environ.get('OLLAMA_HOST', 'http://localhost:11434')
print(f"Connecting to: {ollama_host}", file=sys.stderr)

client = Client(host=ollama_host)

# テストメッセージ
test_message = "Hello! Please respond with a simple greeting in one sentence."

print(f"Sending message to gemma3n:e4b...", file=sys.stderr)
print(f"Message: {test_message}", file=sys.stderr)
print("-" * 60, file=sys.stderr)

try:
    response = client.generate(
        model='gemma3n:e4b',
        prompt=test_message,
        options={
            'num_predict': 100,
            'temperature': 0.7,
        },
    )

    print(f"\nResponse:", file=sys.stderr)
    print("=" * 60)
    print(response['response'])
    print("=" * 60)

except Exception as e:
    print(f"Error: {e}", file=sys.stderr)
    sys.exit(1)
