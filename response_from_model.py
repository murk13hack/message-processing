import requests
import json

def gigachat_request(prompt, text, access_token):
    url = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"

    payload = json.dumps({
    "model": "GigaChat",
    "messages": [
        {
        "role": "system",
        "content": prompt
        },
        {
        "role": "user",
        "content": text
        }
    ],
    "stream": False,
    "update_interval": 0
    })
    headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    'Authorization': f'Bearer {access_token}'
    }

    response = requests.post(url, headers=headers, data=payload)

    return response.json()