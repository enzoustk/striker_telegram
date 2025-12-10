import time
import requests

"""
Editar ou Enviar Mensagens do Telegram
"""


def send(
    message: str,
    chat_id: str,
    token: str,
    parse_mode: str = "MarkdownV2",
    hide_web_page_preview: bool = True,
    verbose: bool = True,
    ) -> tuple:

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    data = {
        "chat_id": chat_id,
        "text": message,
        "disable_web_page_preview": hide_web_page_preview,
        "parse_mode": parse_mode
    }

    response = requests.post(url, data=data)
    
    try:
        response_data = response.json()
    
    except ValueError:
        print("Telegram answered a non-json data")
        print(response.text)
        return None, None

    if response.ok and response_data.get('ok'):      
        message_id = response_data['result']['message_id']
        
        if verbose:
            print(f"Telegram message sent successfully. ID: {message_id}")
        
        return message_id, chat_id

    # checa rate limit via status_code
    elif response.status_code == 429:
        print("Too Many Requests, sleeping...")
        retry_after = response_data.get("parameters", {}).get("retry_after", 60)
        time.sleep(retry_after + 1)
        return None, None

    else:# erro genérico
        print("Telegram message not sent")
        print(f"Status code: {response.status_code}")
        print(f"Response: {response_data}")
    return None, None


def edit(
    message_id: str,
    message: str, 
    chat_id: str ,
    token: str,
    parse_mode: str = "MarkdownV2",
    hide_web_page_preview: bool = True,
    verbose: bool = True,
    ) -> bool:

    url = f"https://api.telegram.org/bot{token}/editMessageText"
    data = {
        "chat_id": chat_id,
        "message_id": message_id,
        "text": message,
        "parse_mode": parse_mode,
        "disable_web_page_preview": hide_web_page_preview
    }

    response = requests.post(url, data=data)
    try:
        response_data = response.json()
    
    except ValueError:
        print(f"Error Trying to edit message id {message_id}: {response.text}")
        return False

    if response.ok and response_data.get('ok'):
        if verbose:
            print(f"Message {message_id} edited successfully.")
        return True

    if response.status_code == 429:
        print("Too Many Requests ao editar, sleeping...")
        retry_after = response_data.get("parameters", {}).get("retry_after", 60)
        time.sleep(retry_after + 1)
        return False

    print(f"Error editing message {message_id}: {response.status_code} - {response_data}")
    return False

