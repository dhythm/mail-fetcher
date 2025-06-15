# Mail Fetcher

Python を使用してメールサーバーからメールを取得するシンプルなプログラムです。

## 機能

- IMAP over SSL/TLS を使用した安全な接続
- 環境変数を使用した認証情報の管理
- 最新のメールを指定した件数分取得
- メールの件名、送信者、日時、本文の表示
- 日本語を含む MIME エンコードされたメールの適切な処理

## 必要要件

- Python 3.10 以上
- インターネット接続
- メールアカウントの IMAP アクセス権限

## セットアップ

1. リポジトリをクローンまたはダウンロード：

```bash
git clone <repository-url>
cd mail-fetcher
```

2. 環境変数を設定：

`.env.example` ファイルをコピーして `.env` ファイルを作成し、必要な情報を記入してください：

```bash
cp .env.example .env
```

必要な環境変数：
- `EMAIL_ADDRESS`: メールアドレス
- `EMAIL_PASSWORD`: メールパスワード（Gmail の場合はアプリパスワード）
- `IMAP_SERVER`: IMAP サーバーのホスト名
- `IMAP_PORT`: IMAP ポート番号（デフォルト: 993）
- `NUM_EMAILS`: 取得するメールの件数（デフォルト: 10）

## 使用方法

環境変数を設定した後、以下のコマンドでプログラムを実行：

```bash
python main.py
```

または、環境変数を直接指定して実行：

```bash
EMAIL_ADDRESS="your-email@example.com" \
EMAIL_PASSWORD="your-password" \
IMAP_SERVER="imap.gmail.com" \
python main.py
```

## 主要なメールプロバイダーの設定

### Gmail
- `IMAP_SERVER`: `imap.gmail.com`
- `IMAP_PORT`: `993`
- **注意**: 2 段階認証を有効にし、アプリパスワードを生成する必要があります
- アプリパスワードの作成: https://support.google.com/accounts/answer/185833

### Outlook/Office 365
- `IMAP_SERVER`: `outlook.office365.com`
- `IMAP_PORT`: `993`

### Yahoo Mail
- `IMAP_SERVER`: `imap.mail.yahoo.com`
- `IMAP_PORT`: `993`

## セキュリティに関する注意事項

- パスワードは環境変数で管理し、コードにハードコーディングしないでください
- `.env` ファイルは `.gitignore` に追加し、バージョン管理に含めないでください
- 本番環境では、より安全な認証方法（OAuth2 など）の使用を検討してください

## トラブルシューティング

### 接続エラーが発生する場合
1. IMAP が有効になっていることを確認してください
2. メールプロバイダーの設定で「安全性の低いアプリ」のアクセスを許可する必要がある場合があります
3. 2 段階認証を使用している場合は、アプリパスワードを生成してください

### 文字化けが発生する場合
プログラムは UTF-8 エンコーディングを使用していますが、一部のメールで文字化けが発生する可能性があります。その場合は、メールのエンコーディング設定を確認してください。

## ライセンス

このプロジェクトは MIT ライセンスの下で公開されています。