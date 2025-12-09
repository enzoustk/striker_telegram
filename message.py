import re
import time
import requests
"""
Editar ou Enviar Mensagens do Telegram
"""


def send_message(
    message: str,
    chat_id: str,
    token: str
    ):

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    data = {
        "chat_id": chat_id,
        "text": message,
        "disable_web_page_preview": True,
        "parse_mode": "MarkdownV2"
    }

    response = requests.post(url, data=data)
    try:
        response_data = response.json()
    except ValueError:
        print("Resposta do Telegram não é JSON:")
        print(response.text)
        return None, None

    if response.ok and response_data.get('ok'):
        message_id = response_data['result']['message_id']
        print(f"Telegram message sent successfully. ID: {message_id}")
        return message_id, chat_id

    # checa rate limit via status_code
    if response.status_code == 429:
        print("Too Many Requests, sleeping...")
        retry_after = response_data.get("parameters", {}).get("retry_after", 60)
        time.sleep(retry_after + 1)
        return None, None

    # erro genérico
    print("Telegram message not sent")
    print(f"Status code: {response.status_code}")
    print(f"Response: {response_data}")
    return None, None


def edit_message(
    message_id: str,
    message: str, 
    chat_id: str ,
    token: str
    ):

    url = f"https://api.telegram.org/bot{token}/editMessageText"
    data = {
        "chat_id": chat_id,
        "message_id": message_id,
        "text": message,
        "parse_mode": "MarkdownV2",
        "disable_web_page_preview": True
    }

    response = requests.post(url, data=data)
    try:
        response_data = response.json()
    except ValueError:
        print(f"Resposta inválida ao editar mensagem {message_id}: {response.text}")
        return False

    if response.ok and response_data.get('ok'):
        print(f"Message {message_id} edited successfully.")
        return True

    if response.status_code == 429:
        print("Too Many Requests ao editar, sleeping...")
        retry_after = response_data.get("parameters", {}).get("retry_after", 60)
        time.sleep(retry_after + 1)
        return False

    print(f"Error editing message {message_id}: {response.status_code} - {response_data}")
    return False


def escape_markdown(
    text
    ) -> str:
    """Escapes MardownV2 special Characters"""

    if type(text) is not str:
            return text
    escape_chars = r'_*[]()~`>#+-=|{}.!'
    return re.sub(f'([{re.escape(escape_chars)}])', r'\\\1', text)
 