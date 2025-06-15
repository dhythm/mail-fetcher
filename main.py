import imaplib
import poplib
import ssl
import email
import email.message
from email.header import decode_header
import os
import sys
import csv
from typing import List, Tuple, Optional, Union
from datetime import datetime
from dotenv import load_dotenv


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


def connect_to_pop3_server(server: str, port: int, email_address: str, password: str) -> poplib.POP3_SSL:
    """POP3サーバーに接続してログインする"""
    try:
        print(f"POP3サーバー {server}:{port} に接続中...")
        
        # SSL接続を確立
        context = ssl.create_default_context()
        mail = poplib.POP3_SSL(server, port, context=context)
        
        # ログイン
        print(f"メールアドレス {email_address} でログイン中...")
        mail.user(email_address)
        mail.pass_(password)
        print("ログイン成功！")
        
        return mail
    except poplib.error_proto as e:
        print(f"POP3接続エラー: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"接続エラー: {e}")
        sys.exit(1)


def fetch_emails_imap(mail: imaplib.IMAP4_SSL, num_emails: int = 10) -> List[Tuple[str, str, str, str]]:
    """IMAPを使用して最新のメールを取得する"""
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


def fetch_emails_pop3(mail: poplib.POP3_SSL, num_emails: int = 10) -> List[Tuple[str, str, str, str]]:
    """POP3を使用して最新のメールを取得する"""
    emails = []
    
    try:
        # メールボックスの統計情報を取得
        num_messages = len(mail.list()[1])
        if num_messages == 0:
            print("メールが見つかりませんでした。")
            return emails
        
        # 取得するメールの数を決定
        start_index = max(1, num_messages - num_emails + 1)
        end_index = num_messages + 1
        
        print(f"\n最新の{min(num_emails, num_messages)}件のメールを取得中...")
        
        # 最新のメールから順に取得（逆順）
        for i in range(num_messages, start_index - 1, -1):
            try:
                # メールを取得
                raw_email_lines = mail.retr(i)[1]
                raw_email = b'\n'.join(raw_email_lines)
                msg = email.message_from_bytes(raw_email)
                
                # ヘッダー情報を取得
                subject = decode_mime_header(msg.get('Subject', '(件名なし)'))
                from_addr = decode_mime_header(msg.get('From', '(送信者不明)'))
                date_str = msg.get('Date', '')
                
                # 本文を取得
                body = get_email_body(msg)
                
                emails.append((subject, from_addr, date_str, body))
                
                if len(emails) >= num_emails:
                    break
                    
            except Exception as e:
                print(f"メール {i} の取得中にエラーが発生しました: {e}")
                continue
                
        return emails
        
    except Exception as e:
        print(f"メール取得エラー: {e}")
        return emails


def export_emails_to_csv(emails: List[Tuple[str, str, str, str]]) -> str:
    """取得したメールをCSVファイルに出力する"""
    if not emails:
        print("出力するメールがありません。")
        return ""
    
    # ファイル名にタイムスタンプを含める
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"emails_{timestamp}.csv"
    
    try:
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            
            # ヘッダー行を書き込み
            writer.writerow(['件名', '送信者', '日時', '本文プレビュー', '本文全体'])
            
            # メールデータを書き込み
            for subject, from_addr, date_str, body in emails:
                # 本文プレビュー（200文字まで）
                body_preview = body[:200] + "..." if len(body) > 200 else body
                # 改行文字を削除して一行にまとめる
                body_preview = body_preview.replace('\n', ' ').replace('\r', ' ')
                body_full = body.replace('\n', ' ').replace('\r', ' ')
                
                writer.writerow([subject, from_addr, date_str, body_preview, body_full])
        
        print(f"メールデータをCSVファイルに出力しました: {filename}")
        return filename
        
    except Exception as e:
        print(f"CSV出力エラー: {e}")
        return ""


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
    
    # .envファイルを読み込み（既存の環境変数を上書き）
    load_dotenv(override=True)
    
    # 環境変数から設定を取得
    protocol = get_env_variable('PROTOCOL', 'IMAP').upper()
    email_address = get_env_variable('EMAIL_ADDRESS')
    email_password = get_env_variable('EMAIL_PASSWORD')
    num_emails = int(get_env_variable('NUM_EMAILS', '10'))
    
    if protocol == 'IMAP':
        # IMAP設定
        server = get_env_variable('IMAP_SERVER')
        port = int(get_env_variable('IMAP_PORT', '993'))
        
        # IMAPサーバーに接続
        mail = connect_to_imap_server(server, port, email_address, email_password)
        
        try:
            # メールを取得
            emails = fetch_emails_imap(mail, num_emails)
            
            # メールを表示
            display_emails(emails)
            
            # CSVファイルに出力
            export_emails_to_csv(emails)
            
        finally:
            # 接続を閉じる
            try:
                mail.close()
                mail.logout()
                print("接続を終了しました。")
            except:
                pass
                
    elif protocol == 'POP3':
        # POP3設定
        server = get_env_variable('POP3_SERVER')
        port = int(get_env_variable('POP3_PORT', '995'))
        
        # POP3サーバーに接続
        mail = connect_to_pop3_server(server, port, email_address, email_password)
        
        try:
            # メールを取得
            emails = fetch_emails_pop3(mail, num_emails)
            
            # メールを表示
            display_emails(emails)
            
            # CSVファイルに出力
            export_emails_to_csv(emails)
            
        finally:
            # 接続を閉じる
            try:
                mail.quit()
                print("接続を終了しました。")
            except:
                pass
    else:
        print(f"エラー: サポートされていないプロトコル '{protocol}' が指定されました。")
        print("PROTOCOL環境変数には 'IMAP' または 'POP3' を指定してください。")
        sys.exit(1)


if __name__ == "__main__":
    main()