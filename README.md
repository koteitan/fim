# CodeGemma FIM (Fill-In-the-Middle) Example

OllamaとCodeGemmaを使用したFIM（Fill-In-the-Middle）のサンプル実装です。

## 環境

- **Ollama**: Windows上でホスト
- **WSL2**: Pythonスクリプトを実行
- **接続**: 環境変数`OLLAMA_HOST`でOllamaサーバーのURLを指定

## セットアップ

```bash
# 依存パッケージのインストール
pip install ollama

# CodeGemmaモデルのダウンロード
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

## 現在の問題 ⚠️

**OllamaでのFIM（Fill-In-the-Middle）機能が動作しません。**

### テスト結果サマリー

| モデル | テスト1<br>import文補完<br>(FIM) | テスト2<br>関数本体補完<br>(FIM) | テスト3<br>関数本体補完<br>(FIMなし) |
|--------|------|------|------|
| **CodeGemma 2B** | ❌ suffixを無視<br>18行の無関係なimport | ❌ 空の出力 | ✅ 正常動作<br>`print("Hello World")` |
| **CodeGemma 7B** | ❌ 空の出力 | ❌ 空の出力 | ✅ 正常動作<br>`print('Hello World')`<br>(18回繰り返し) |
| **StarCoder2 7B** | ❌ suffixを無視<br>無関係な関数定義 | ❌ 空の出力 | ⚠️ 部分的に動作<br>`print_hello_world()` |

**結論:**
- ✅ **FIMなし**: 両モデルとも通常の補完は動作
- ❌ **FIMあり**: 両モデルともsuffixを完全に無視または空の出力

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

**StarCoder2 7B の出力:**
```python


def hello():
    print("hello")

```
→ **suffixを無視**、無関係な関数定義

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

### 通常のコード補完は動作

FIMは動作しませんが、通常のコード補完（prefixのみ）は正常に動作します：
```bash
python3 python/chat.py  # 通常のチャットは動作確認済み
```

## 参考資料

- [CodeGemma公式ドキュメント](https://ai.google.dev/gemma/docs/codegemma)
- [Ollama CodeGemmaページ](https://ollama.com/library/codegemma)
- [CodeGemmaプロンプト構造](https://ai.google.dev/gemma/docs/codegemma/prompt-structure)

## ファイル構成

- `python/fim.py` - FIMのサンプル実装（公式フォーマット）
- `python/chat.py` - Ollama接続テスト用チャットスクリプト
- `CLAUDE.md` - プロジェクト固有のルール


