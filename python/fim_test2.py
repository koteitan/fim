#!/usr/bin/env python3
"""
FIM Test 2: Function body completion
Supports: CodeGemma and StarCoder2
"""
from ollama import generate
import os
import sys
import argparse

# Ollamaサーバーに接続（環境変数で指定可能、デフォルトはlocalhost）
os.environ.setdefault('OLLAMA_HOST', 'http://localhost:11434')

# コマンドライン引数のパース
parser = argparse.ArgumentParser(description='FIM Test 2: Function body completion')
parser.add_argument('--model', '-m',
                    choices=['codegemma:2b-code', 'codegemma:7b-code', 'starcoder2:3b', 'starcoder2:7b', 'starcoder2:15b', 'codellama:7b-code', 'codellama:13b-code', 'codellama:34b-code'],
                    default='codegemma:2b-code',
                    help='Model to use for FIM (default: codegemma:2b-code)')
parser.add_argument('--temp', '-t', type=float, default=0,
                    help='Temperature (default: 0)')
parser.add_argument('--method', choices=['suffix', 'manual', 'both'], default='both',
                    help='FIM method: suffix (Ollama template), manual (manual tokens), both (default: both)')
args = parser.parse_args()

# FIM example: complete the function body
prefix = 'def print_hello_world():\n    '
suffix = '\n\nprint_hello_world()'

print(f"Model: {args.model}")
print(f"Temperature: {args.temp}")
print(f"Method: {args.method}")
print(f"Prefix: {repr(prefix)}")
print(f"Suffix: {repr(suffix)}")
print("=" * 60)

# Method 1: Ollama templateを使用（suffix parameter）
if args.method in ['suffix', 'both']:
    print("\n[Method 1] Using Ollama template (suffix parameter)")
    try:
        response = generate(
            model=args.model,
            prompt=prefix,
            suffix=suffix.strip(),
            options={
                'num_predict': 128,
                'temperature': args.temp,
                'top_p': 0.9,
                'stop': ['<|file_separator|>'],
            },
        )

        print("Generated code:")
        print(response.response)
        print("=" * 60)
        print(f"Result: {response.response[:80] if response.response else '(empty)'}...")

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)

# Method 2: 手動でFIMトークンを埋め込み（公式推奨）
if args.method in ['manual', 'both']:
    print("\n[Method 2] Manual FIM tokens (official recommended)")

    # モデルごとにFIMトークンが異なる
    if 'codegemma' in args.model:
        fim_prompt = f'<|fim_prefix|>{prefix}<|fim_suffix|>{suffix}<|fim_middle|>'
        stop_tokens = ['<|file_separator|>', '<|fim_prefix|>', '<|fim_suffix|>', '<|fim_middle|>']
    elif 'codellama' in args.model:
        fim_prompt = f'<PRE> {prefix} <SUF>{suffix} <MID>'
        stop_tokens = ['', '<PRE>', '<SUF>', '<MID>']
    else:  # starcoder2
        fim_prompt = f'<fim_prefix>{prefix}<fim_suffix>{suffix}<fim_middle>'
        stop_tokens = ['<fim_prefix>', '<fim_suffix>', '<fim_middle>', '<file_sep>']

    print(f"FIM Prompt: {repr(fim_prompt[:100])}...")

    try:
        response = generate(
            model=args.model,
            prompt=fim_prompt,
            options={
                'num_predict': 128,
                'temperature': args.temp,
                'top_p': 0.9,
                'stop': stop_tokens,
            },
        )

        print("Generated code:")
        print(response.response)
        print("=" * 60)
        print(f"Result: {response.response[:80] if response.response else '(empty)'}...")

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)

print("\n" + "=" * 60)
print("Expected: print(\"Hello world\") or similar")
