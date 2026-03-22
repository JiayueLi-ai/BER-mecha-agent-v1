from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import os
import sys
import json

try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

SCOPES = ['https://www.googleapis.com/auth/gmail.modify']
TOKEN_PATH = 'token.json'
CRED_PATH = 'credentials.json'
LABEL_AI_CHECKED = 'ai-checked'
MAX_RESULTS = 50


def get_service():
    creds = None
    if os.path.exists(TOKEN_PATH):
        creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CRED_PATH, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(TOKEN_PATH, 'w', encoding='utf-8') as f:
            f.write(creds.to_json())
    return build('gmail', 'v1', credentials=creds)


def get_header(headers, name):
    for h in headers or []:
        if h.get('name', '').lower() == name.lower():
            return h.get('value', '')
    return ''


def get_or_create_label_id(service, label_name):
    labels = service.users().labels().list(userId='me').execute().get('labels', [])
    for lb in labels:
        if lb.get('name') == label_name:
            return lb.get('id')
    created = service.users().labels().create(
        userId='me',
        body={
            'name': label_name,
            'labelListVisibility': 'labelShow',
            'messageListVisibility': 'show'
        }
    ).execute()
    return created.get('id')


# ========== 模式1：获取邮件列表（无参数时） ==========
def fetch_emails(service):
    # 先获取 ai-checked 的标签ID
    ai_checked_id = get_or_create_label_id(service, LABEL_AI_CHECKED)

    # 只用 is:unread 查询，然后在代码里手动过滤掉有 ai-checked 标签的邮件
    resp = service.users().messages().list(userId='me', q='is:unread', maxResults=200).execute()
    messages = resp.get('messages', [])

    if not messages:
        print(json.dumps([], ensure_ascii=False))
        return

    email_list = []
    for msg in messages:
        detail = service.users().messages().get(
            userId='me',
            id=msg['id'],
            format='metadata',
            metadataHeaders=['Subject', 'From', 'Date']
        ).execute()

        # 用标签ID判断，跳过已有 ai-checked 的邮件
        label_ids = detail.get('labelIds', [])
        if ai_checked_id in label_ids:
            continue

        headers = detail.get('payload', {}).get('headers', [])
        email_list.append({
            'id': msg['id'],
            'subject': get_header(headers, 'Subject') or '(无标题)',
            'from': get_header(headers, 'From'),
            'date': get_header(headers, 'Date'),
            'snippet': detail.get('snippet', '')[:100]
        })

        if len(email_list) >= MAX_RESULTS:
            break

    print(json.dumps(email_list, ensure_ascii=False, indent=2))


# ========== 模式2：给单封邮件打标签（传入 message_id + category 时） ==========
def label_email(service, message_id, category):
    # 确认是未读邮件
    msg = service.users().messages().get(userId='me', id=message_id).execute()
    if 'UNREAD' not in msg.get('labelIds', []):
        print(f'Skip (already read): {message_id}')
        return

    ai_checked_id = get_or_create_label_id(service, LABEL_AI_CHECKED)
    category_id = get_or_create_label_id(service, category)

    service.users().messages().modify(
        userId='me',
        id=message_id,
        body={
            'addLabelIds': [ai_checked_id, category_id]
            # 不移除 UNREAD，不移除 INBOX，状态保持不变
        }
    ).execute()

    print(f'OK {message_id} -> {category}')


# ========== 入口 ==========
def main():
    service = get_service()

    if len(sys.argv) == 1:
        # 无参数 → 获取邮件列表
        fetch_emails(service)
    elif len(sys.argv) == 3:
        # 传入 message_id + category → 打标签
        label_email(service, sys.argv[1], sys.argv[2])
    else:
        print('用法：')
        print('  获取邮件列表: python gmail_assistant.py')
        print('  打标签:       python gmail_assistant.py "<message_id>" "<category>"')
        sys.exit(1)


if __name__ == '__main__':
    main()
