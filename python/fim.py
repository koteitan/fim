#!/usr/bin/env python3
"""
FIM (Fill-In-the-Middle) Sample for Ollama
Supports: CodeGemma and StarCoder2
"""
from ollama import generate
import os
import sys
import argparse

# Ollamaサーバーに接続（環境変数で指定可能、デフォルトはlocalhost）
os.environ.setdefault('OLLAMA_HOST', 'http://localhost:11434')

# コマンドライン引数のパース
parser = argparse.ArgumentParser(description='FIM (Fill-In-the-Middle) test with Ollama')
parser.add_argument('--model', '-m',
                    choices=['codegemma:2b-code', 'codegemma:7b-code', 'starcoder2:3b', 'starcoder2:7b', 'starcoder2:15b'],
                    default='codegemma:2b-code',
                    help='Model to use for FIM (default: codegemma:2b-code)')
parser.add_argument('--temp', '-t', type=float, default=0.3,
                    help='Temperature (default: 0.3)')
args = parser.parse_args()

# FIM example: complete the missing import statement
prefix = 'import '
suffix = '''
if __name__ == "__main__":
    sys.exit(0)'''

print(f"Model: {args.model}")
print(f"Temperature: {args.temp}")
print(f"Prefix: {repr(prefix)}")
print(f"Suffix: {repr(suffix)}")
print("=" * 60)

# Ollama templateを使用（suffix parameter）
print("Mode: Using Ollama template (suffix parameter)")
try:
    response = generate(
        model=args.model,
        prompt=prefix,  # prefix部分のみ
        suffix=suffix.strip(),  # suffix部分
        options={
            'num_predict': 128,
            'temperature': args.temp,
            'top_p': 0.9,
        },
    )

    print("Generated code:")
    print(response.response)
    print("=" * 60)

    # 期待される結果
    print("\nExpected: 'sys' (or similar context-aware completion)")
    print(f"Got: {response.response[:80]}...")

except Exception as e:
    print(f"Error: {e}", file=sys.stderr)
    sys.exit(1)


