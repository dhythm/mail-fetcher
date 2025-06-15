import imaplib
import ssl
import email
from email.header import decode_header
import os
import sys
from typing import List, Tuple, Optional
from datetime import datetime


def get_env_variable(var_name: str, default: Optional[str] = None) -> str:
    """環境変数を取得する。存在しない場合はエラーを出力して終了。"""
    value = os.environ.get(var_name, default)
    if value is None:
        print(f"エラー: 環境変数 {var_name} が設定されていません。")
        sys.exit(1)
    return value


def decode_mime_header(header: str) -> str:
    """MIMEエンコードされたヘッダーをデコードする"""
    decoded_parts = []
    for part, encoding in decode_header(header):
        if isinstance(part, bytes):
            decoded_parts.append(part.decode(encoding or 'utf-8', errors='replace'))
        else:
            decoded_parts.append(part)
    return ''.join(decoded_parts)


def get_email_body(msg: email.message.Message) -> str:
    """メールの本文を取得する"""
    body = ""
    
    if msg.is_multipart():
        for part in msg.walk():
            content_type = part.get_content_type()
            content_disposition = str(part.get("Content-Disposition"))
            
            if content_type == "text/plain" and "attachment" not in content_disposition:
                try:
                    body = part.get_payload(decode=True).decode('utf-8', errors='replace')
                    break
                except:
                    pass
    else:
        try:
            body = msg.get_payload(decode=True).decode('utf-8', errors='replace')
        except:
            body = str(msg.get_payload())
    
    return body.strip()


def connect_to_imap_server(server: str, port: int, email_address: str, password: str) -> imaplib.IMAP4_SSL:
    """IMAPサーバーに接続してログインする"""
    try:
        print(f"IMAPサーバー {server}:{port} に接続中...")
        
        # SSL接続を確立
        context = ssl.create_default_context()
        mail = imaplib.IMAP4_SSL(server, port, ssl_context=context)
        
        # ログイン
        print(f"メールアドレス {email_address} でログイン中...")
        mail.login(email_address, password)
        print("ログイン成功！")
        
        return mail
    except imaplib.IMAP4.error as e:
        print(f"IMAP接続エラー: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"接続エラー: {e}")
        sys.exit(1)


def fetch_emails(mail: imaplib.IMAP4_SSL, num_emails: int = 10) -> List[Tuple[str, str, str, str]]:
    """最新のメールを取得する"""
    emails = []
    
    try:
        # 受信箱を選択
        mail.select('INBOX')
        
        # メールIDを検索（全てのメール）
        status, messages = mail.search(None, 'ALL')
        if status != 'OK':
            print("メールの検索に失敗しました。")
            return emails
        
        # メールIDのリストを取得
        mail_ids = messages[0].split()
        if not mail_ids:
            print("メールが見つかりませんでした。")
            return emails
        
        # 最新のメールから指定数だけ取得
        latest_email_ids = mail_ids[-num_emails:] if len(mail_ids) >= num_emails else mail_ids
        latest_email_ids.reverse()  # 最新のメールを先頭に
        
        print(f"\n最新の{len(latest_email_ids)}件のメールを取得中...")
        
        for i, email_id in enumerate(latest_email_ids):
            # メールを取得
            status, msg_data = mail.fetch(email_id, '(RFC822)')
            if status != 'OK':
                continue
            
            # メールをパース
            raw_email = msg_data[0][1]
            msg = email.message_from_bytes(raw_email)
            
            # ヘッダー情報を取得
            subject = decode_mime_header(msg.get('Subject', '(件名なし)'))
            from_addr = decode_mime_header(msg.get('From', '(送信者不明)'))
            date_str = msg.get('Date', '')
            
            # 本文を取得
            body = get_email_body(msg)
            
            emails.append((subject, from_addr, date_str, body))
            
        return emails
        
    except Exception as e:
        print(f"メール取得エラー: {e}")
        return emails


def display_emails(emails: List[Tuple[str, str, str, str]]) -> None:
    """取得したメールを表示する"""
    if not emails:
        print("表示するメールがありません。")
        return
    
    print(f"\n{'='*80}")
    print(f"取得したメール: {len(emails)}件")
    print(f"{'='*80}\n")
    
    for i, (subject, from_addr, date_str, body) in enumerate(emails, 1):
        print(f"[メール {i}]")
        print(f"件名: {subject}")
        print(f"送信者: {from_addr}")
        print(f"日時: {date_str}")
        print(f"本文:")
        print("-" * 40)
        # 本文の最初の200文字を表示
        body_preview = body[:200] + "..." if len(body) > 200 else body
        print(body_preview)
        print(f"\n{'='*80}\n")


def main():
    """メイン処理"""
    print("メール取得プログラムを開始します...\n")
    
    # 環境変数から設定を取得
    email_address = get_env_variable('EMAIL_ADDRESS')
    email_password = get_env_variable('EMAIL_PASSWORD')
    imap_server = get_env_variable('IMAP_SERVER')
    imap_port = int(get_env_variable('IMAP_PORT', '993'))
    num_emails = int(get_env_variable('NUM_EMAILS', '10'))
    
    # IMAPサーバーに接続
    mail = connect_to_imap_server(imap_server, imap_port, email_address, email_password)
    
    try:
        # メールを取得
        emails = fetch_emails(mail, num_emails)
        
        # メールを表示
        display_emails(emails)
        
    finally:
        # 接続を閉じる
        try:
            mail.close()
            mail.logout()
            print("接続を終了しました。")
        except:
            pass


if __name__ == "__main__":
    main()