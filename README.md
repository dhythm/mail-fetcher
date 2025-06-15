# Mail Fetcher

Python を使用してメールサーバーからメールを取得するシンプルなプログラムです。

## 機能

- IMAP および POP3 プロトコルに対応
- SSL/TLS を使用した安全な接続
- 環境変数を使用した認証情報の管理
- 最新のメールを指定した件数分取得
- メールの件名、送信者、日時、本文の表示
- 日本語を含む MIME エンコードされたメールの適切な処理

## 必要要件

- Python 3.10 以上
- インターネット接続
- メールアカウントの IMAP または POP3 アクセス権限

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
- `PROTOCOL`: 使用するプロトコル（`IMAP` または `POP3`、デフォルト: `IMAP`）
- `EMAIL_ADDRESS`: メールアドレス
- `EMAIL_PASSWORD`: メールパスワード（Gmail の場合はアプリパスワード）
- `NUM_EMAILS`: 取得するメールの件数（デフォルト: 10）

IMAP 使用時：
- `IMAP_SERVER`: IMAP サーバーのホスト名
- `IMAP_PORT`: IMAP ポート番号（デフォルト: 993）

POP3 使用時：
- `POP3_SERVER`: POP3 サーバーのホスト名
- `POP3_PORT`: POP3 ポート番号（デフォルト: 995）

## 使用方法

環境変数を設定した後、以下のコマンドでプログラムを実行：

```bash
uv run main.py
```

または、環境変数を直接指定して実行：

IMAP の場合：
```bash
PROTOCOL="IMAP" \
EMAIL_ADDRESS="your-email@example.com" \
EMAIL_PASSWORD="your-password" \
IMAP_SERVER="imap.gmail.com" \
uv run main.py
```

POP3 の場合：
```bash
PROTOCOL="POP3" \
EMAIL_ADDRESS="your-email@example.com" \
EMAIL_PASSWORD="your-password" \
POP3_SERVER="pop.gmail.com" \
uv run main.py
```

## 主要なメールプロバイダーの設定

### Gmail
IMAP:
- `IMAP_SERVER`: `imap.gmail.com`
- `IMAP_PORT`: `993`

POP3:
- `POP3_SERVER`: `pop.gmail.com`
- `POP3_PORT`: `995`

**注意**: 
- 2 段階認証を有効にし、アプリパスワードを生成する必要があります
- アプリパスワードの作成: https://support.google.com/accounts/answer/185833
- Gmail の設定で IMAP/POP アクセスを有効にする必要があります

### Outlook/Office 365
IMAP:
- `IMAP_SERVER`: `outlook.office365.com`
- `IMAP_PORT`: `993`

POP3:
- `POP3_SERVER`: `outlook.office365.com`
- `POP3_PORT`: `995`

### Yahoo Mail
IMAP:
- `IMAP_SERVER`: `imap.mail.yahoo.com`
- `IMAP_PORT`: `993`

POP3:
- `POP3_SERVER`: `pop.mail.yahoo.com`
- `POP3_PORT`: `995`

## セキュリティに関する注意事項

- パスワードは環境変数で管理し、コードにハードコーディングしないでください
- `.env` ファイルは `.gitignore` に追加し、バージョン管理に含めないでください
- 本番環境では、より安全な認証方法（OAuth2 など）の使用を検討してください

## IMAP と POP3 の違い

### IMAP（Internet Message Access Protocol）
- サーバー上のメールを管理
- 複数のデバイスから同じメールボックスにアクセス可能
- フォルダ（ラベル）の操作が可能
- 既読/未読の状態が同期される

### POP3（Post Office Protocol version 3）
- メールをローカルにダウンロード
- 通常、ダウンロード後はサーバーから削除（設定により変更可能）
- シンプルなプロトコル
- フォルダ操作は不可

## トラブルシューティング

### 接続エラーが発生する場合
1. IMAP/POP3 が有効になっていることを確認してください
2. メールプロバイダーの設定で「安全性の低いアプリ」のアクセスを許可する必要がある場合があります
3. 2 段階認証を使用している場合は、アプリパスワードを生成してください
4. ファイアウォールがポート 993（IMAP）または 995（POP3）をブロックしていないか確認してください

### 文字化けが発生する場合
プログラムは UTF-8 エンコーディングを使用していますが、一部のメールで文字化けが発生する可能性があります。その場合は、メールのエンコーディング設定を確認してください。

## ライセンス

このプロジェクトは MIT ライセンスの下で公開されています。