# CLAUDE.md

このファイルは、AI アシスタント Claude Code がこのプロジェクトをより効果的にサポートするための情報を含んでいます。

## プロジェクト概要

Mail Fetcher は Python を使用してメールサーバーからメールを取得し、OpenAI API を使って技術案件情報を分析するプログラムです。IMAP および POP3 プロトコルに対応し、SSL/TLS を使用した安全な接続でメールを取得できます。分析結果はCSVファイルに出力されます。

## ファイル構成

- `main.py`: メイン処理を含むファイル。IMAP/POP3 接続、メール取得、表示機能を実装
- `pyproject.toml`: プロジェクト設定ファイル（uv を使用）
- `README.md`: プロジェクトのドキュメント

## 実行コマンド

### 基本実行
```bash
uv run main.py
```

### 環境変数を直接指定（IMAP）
```bash
PROTOCOL="IMAP" \
EMAIL_ADDRESS="your-email@example.com" \
EMAIL_PASSWORD="your-password" \
IMAP_SERVER="imap.gmail.com" \
uv run main.py
```

### 環境変数を直接指定（POP3）
```bash
PROTOCOL="POP3" \
EMAIL_ADDRESS="your-email@example.com" \
EMAIL_PASSWORD="your-password" \
POP3_SERVER="pop.gmail.com" \
uv run main.py
```

### AI分析機能付きで実行（IMAP）
```bash
PROTOCOL="IMAP" \
EMAIL_ADDRESS="your-email@example.com" \
EMAIL_PASSWORD="your-password" \
IMAP_SERVER="imap.gmail.com" \
OPENAI_API_KEY="your-openai-api-key" \
uv run main.py
```

## 必要な環境変数

### 共通
- `PROTOCOL`: `IMAP` または `POP3`（デフォルト: `IMAP`）
- `EMAIL_ADDRESS`: メールアドレス
- `EMAIL_PASSWORD`: メールパスワード
- `NUM_EMAILS`: 取得するメール件数（デフォルト: 10）

### IMAP用
- `IMAP_SERVER`: IMAP サーバーホスト名
- `IMAP_PORT`: IMAP ポート番号（デフォルト: 993）

### POP3用
- `POP3_SERVER`: POP3 サーバーホスト名
- `POP3_PORT`: POP3 ポート番号（デフォルト: 995）

### AI分析機能用（オプション）
- `OPENAI_API_KEY`: OpenAI API キー（設定した場合のみAI分析が実行される）
- `OPENAI_MODEL`: 使用するOpenAIモデル（デフォルト: `gpt-3.5-turbo`）

## 技術詳細

- **Python バージョン**: 3.10 以上
- **使用ライブラリ**: 標準ライブラリ（imaplib, poplib, ssl, email など）+ openai, python-dotenv
- **パッケージ管理**: uv を使用
- **文字エンコーディング**: UTF-8、MIME エンコード対応

## 主要機能

1. **プロトコル対応**: IMAP/POP3 両方をサポート
2. **セキュア接続**: SSL/TLS を使用した暗号化通信
3. **文字化け対策**: 日本語を含む MIME エンコードされたメールの適切な処理
4. **本文取得**: マルチパート/プレーンテキスト両方に対応
5. **AI分析**: OpenAI API を使用した技術案件情報の自動抽出
6. **データ出力**: 分析結果をCSV形式で出力
7. **エラーハンドリング**: 接続エラーや認証エラーの適切な処理

## よくある対応

- Gmail アカウントの場合、2段階認証とアプリパスワードが必要
- メールプロバイダーによって IMAP/POP3 の有効化設定が必要
- 環境変数は `.env` ファイルで管理可能（`.env.example` を参考）