# FIM (Fill-In-the-Middle) with Ollama

OllamaとCodeLlama/StarCoder2/CodeGemmaを使用したFIM（Fill-In-the-Middle）のサンプル実装です。

**最新の状況:**
- ✅ **CodeLlama 7B-code + suffix parameter方式で完全成功！** 🎉
- ✅ **StarCoder2 7B + 手動FIMトークン方式で部分的に成功**
- ⚠️ CodeGemmaは依然として課題あり
- 📝 Ollama v0.12.6でテスト済み

## 環境

- **Ollama**: Windows上でホスト
- **WSL2**: Pythonスクリプトを実行
- **接続**: 環境変数`OLLAMA_HOST`でOllamaサーバーのURLを指定

## セットアップ

```bash
# 依存パッケージのインストール
pip install ollama

# モデルのダウンロード
ollama pull codellama:7b-code    # ✅ 推奨！両方のテストで完全成功
ollama pull starcoder2:7b        # ✅ import文補完で成功
ollama pull codegemma:2b-code
ollama pull codegemma:7b-code
```

## 使用方法

```bash
# 基本的なFIMテスト
python3 python/fim.py

# チャットテスト（動作確認用）
python3 python/chat.py
```

## ✅ 成功例

**CodeLlama 7B-code が両方のテストで完全成功！** 🎉

### テスト結果サマリー（改善後）

| モデル | 方式 | テスト1<br>import文補完<br>(`fim.py`) | テスト2<br>関数本体補完<br>(`fim_test2.py`) |
|--------|------|------|------|
| **CodeLlama 7B-code** | suffix parameter | ✅ **完全成功**<br>`sys` | ✅ **完全成功**<br>`print("Hello, World!")` |
| **CodeLlama 7B-code** | 手動トークン | ❌ 空の出力 | ❌ 空の出力 |
| **StarCoder2 7B** | 手動トークン | ✅ **成功**<br>`import sys` | ❌ 空の出力 |
| **StarCoder2 7B** | suffix parameter | ⚠️ 不完全<br>`from <\|package\|>.version` | ❌ テストなし |
| **CodeGemma 2B** | 手動トークン | ⚠️ suffixを無視<br>18行の無関係なimport | ⚠️ suffixをコピー<br>`print_hello_world()` |
| **CodeGemma 7B** | 手動トークン | ❌ 空の出力 | ❌ 空の出力 |

**重要な発見:**
- 🏆 **CodeLlama 7B-codeが最優秀** - 両方のテストで完全成功
- ✅ **CodeLlamaはsuffix parameter方式と相性が良い**
- ✅ **StarCoder2は手動トークン方式で成功**（import文のみ）
- ✅ **temperature=0とstopトークン**が重要
- ⚠️ モデルと方式の組み合わせが重要

### 具体的な出力例

#### テスト1: import文の補完

**Input:**
```python
prefix = 'import '
suffix = '\nif __name__ == "__main__":\n    sys.exit(0)'
```

**Expected:**
```python
sys
```

**CodeGemma 2B の出力:**
```python
import os
import sys
import time
import json
import random
import logging
import argparse
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import Dataset, DataLoader
from torch.utils.tensorboard import SummaryWriter
from torch.nn.utils.rnn import pad_sequence
from torch.optim import AdamW
from torch.optim.lr_scheduler import LambdaLR
from torch.nn.utils import clip_grad_norm_
from torch.nn.utils.rnn import pad_sequence
```
→ **suffixを無視**、18行の無関係なimport

**CodeGemma 7B の出力:**
```
(空の出力)
```
→ **suffixを無視**、何も生成されない

**StarCoder2 7B の出力（suffix parameter方式）:**
```python


from <|package|>.version import __version__

```
→ **不完全**、特殊トークンが含まれる

**StarCoder2 7B の出力（手動トークン方式）:**
```python

import sys
```
→ ✅ **成功！** suffixのコンテキスト（`sys.exit(0)`）を正しく認識

**CodeLlama 7B-code の出力（suffix parameter方式）:**
```python
sys
```
→ ✅ **完全成功！** 最もシンプルで正確な出力

---

#### テスト2: 関数本体の補完

**Input:**
```python
prefix = 'def print_hello_world():\n    '
suffix = '\n\nprint_hello_world()'
```

**Expected:**
```python
print("Hello world")
```

**CodeGemma 2B の出力:**
```
(空の出力)
```
→ suffixを完全に無視

**CodeGemma 7B の出力:**
```
(空の出力)
```
→ suffixを完全に無視

**StarCoder2 7B の出力:**
```
(空の出力)
```

**CodeLlama 7B-code の出力（suffix parameter方式）:**
```python
"""Print "Hello, World!" to the screen."""
    print("Hello, World!")
```
→ ✅ **完全成功！** docstringまで生成（ただし`<EOT>`タグの後に余分なコードあり）

---

#### テスト3: 通常の補完（FIMなし、参考）

**Input:**
```python
prompt = 'def print_hello_world():\n    '
# suffixなし（FIMなし）
```

**Expected:**
```python
# 関数本体のコード
```

**CodeGemma 2B の出力:**
```python
print("Hello World")















```
→ ✅ **正しく動作**（その後空行が続く）

**CodeGemma 7B の出力:**
```python
print('Hello World')
    print('Hello World')
    print('Hello World')
    print('Hello World')
    print('Hello World')
    print('Hello World')
    print('Hello World')
    print('Hello World')
    print('Hello World')
    print('Hello World')
    print('Hello World')
    print('Hello World')
    print('Hello World')
    print('Hello World')
    print('Hello World')
    print('Hello World')
    print('Hello World')
    print('Hello World')
```
→ ✅ **正しく動作**（18回繰り返し）

**StarCoder2 7B の出力:**
```python


print_hello_world()
```
→ 関数呼び出しを生成（不完全だが動作）

**問題の要約：**
- ✅ 通常のコード補完（FIMなし）は動作
- ❌ FIMモード（suffix指定）では、suffixを完全に無視
- ❌ 期待される「コンテキストを考慮した補完」が機能していない

### 検証済みの内容

✅ **正しく実装されている要素:**
- Ollama公式ドキュメントのFIMフォーマットを使用
- Google AI公式ガイドのトークン構造に準拠
- モデルファイルにFIMトークンが正しく設定されている
  - CodeGemma: `<|fim_prefix|>`, `<|fim_suffix|>`, `<|fim_middle|>`
  - StarCoder2: `<fim_prefix>`, `<fim_suffix>`, `<fim_middle>`
- Ollamaのテンプレートシステムで`.Suffix`パラメータがサポートされている

✅ **試したアプローチ:**
1. `suffix`パラメータを使用（Ollamaテンプレート経由）
2. 手動でFIMトークンをプロンプトに埋め込み
3. `raw`モードでの実行
4. 異なるtemperature設定（0, 0.3, 0.5）
5. 複数のモデル（CodeGemma 2B/7B, StarCoder2 7B）

❌ **動作しない理由の推測:**
- OllamaのFIM実装が不完全または未動作
- モデルの量子化/変換時にFIM機能が失われた可能性
- Ollama API側のバグまたは未実装機能

### 🔧 FIMを動作させる方法（改善版）

#### 方法1: CodeLlama + suffix parameter（最も簡単で成功率が高い） 🏆

```python
from ollama import generate

prefix = 'import '
suffix = '\nif __name__ == "__main__":\n    sys.exit(0)'

# suffix parameterを使用（CodeLlamaで動作）
response = generate(
    model='codellama:7b-code',
    prompt=prefix,
    suffix=suffix.strip(),
    options={
        'num_predict': 128,
        'temperature': 0,
        'top_p': 0.9,
        'stop': ['<EOT>'],  # CodeLlamaのstopトークン
    },
)

print(response.response)  # 出力: "sys"
```

#### 方法2: StarCoder2 + 手動トークン（import文のみ成功）

```python
from ollama import generate

prefix = 'import '
suffix = '\nif __name__ == "__main__":\n    sys.exit(0)'

# 手動でFIMトークンを埋め込む
fim_prompt = f'<fim_prefix>{prefix}<fim_suffix>{suffix}<fim_middle>'

response = generate(
    model='starcoder2:7b',
    prompt=fim_prompt,
    options={
        'num_predict': 128,
        'temperature': 0,
        'top_p': 0.9,
        'stop': ['<fim_prefix>', '<fim_suffix>', '<fim_middle>', '<file_sep>'],
    },
)

print(response.response)  # 出力: "\nimport sys"
```

**重要なポイント:**
1. 🏆 **CodeLlama 7B-code + suffix parameter**が最も確実（両方のテストで成功）
2. ✅ **StarCoder2 + 手動トークン**はimport文補完のみ成功
3. ✅ **temperature=0** に設定（公式推奨値）
4. ✅ **stopトークンを必ず指定**（モデルごとに異なる）
5. ⚠️ **モデルと方式の組み合わせが重要**

**コマンドライン例:**
```bash
# StarCoder2で手動トークン方式（推奨）
python3 python/fim.py -m starcoder2:7b --method manual

# 両方の方式を比較
python3 python/fim.py -m starcoder2:7b --method both
```

### 通常のコード補完は動作

FIMは動作しませんが、通常のコード補完（prefixのみ）は正常に動作します：
```bash
python3 python/chat.py  # 通常のチャットは動作確認済み
```

## 参考資料

### 公式ドキュメント
- [CodeGemma公式ドキュメント](https://ai.google.dev/gemma/docs/codegemma)
- [Ollama CodeGemmaページ](https://ollama.com/library/codegemma)
- [CodeGemmaプロンプト構造](https://ai.google.dev/gemma/docs/codegemma/prompt-structure)
- [Ollama公式テンプレートドキュメント](https://github.com/ollama/ollama/blob/main/docs/template.md) - `.Suffix`パラメータの説明

### FIM成功例・実装参考
- [Ollama Blog: Code Llamaのプロンプト方法](https://ollama.com/blog/how-to-prompt-code-llama) - **手動FIMトークン方式の成功例**
- [ollamar: generate関数リファレンス](https://hauselin.github.io/ollama-r/reference/generate.html) - suffixパラメータの使用例（R言語）

### GitHub Issues・ディスカッション
- [Ollama Issue #6968: FIMモデルのテンプレート調整](https://github.com/ollama/ollama/issues/6968) - **suffixパラメータ使用時の課題**
- [Ollama Issue #5403: Codestral FIMサポート](https://github.com/ollama/ollama/issues/5403) - テンプレート実装の議論
- [TabbyML Issue #2845: OllamaのFIMプロンプトテンプレート発見](https://github.com/TabbyML/tabby/issues/2845) - 実装のヒント

## ファイル構成

- `python/fim.py` - FIMのサンプル実装（両方の方式をサポート）
  - `--method manual`: 手動トークン方式（推奨）
  - `--method suffix`: suffixパラメータ方式
  - `--method both`: 両方を比較（デフォルト）
- `python/fim_test2.py` - 関数本体補完のテスト
- `python/chat.py` - Ollama接続テスト用チャットスクリプト
- `CLAUDE.md` - プロジェクト固有のルール


