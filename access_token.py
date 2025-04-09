import requests
import base64
import uuid
def get_access_token(client_id, client_secret):
   # URL для получения access token
   url = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"
   # Генерация заголовка авторизации
   auth_key = base64.b64encode(f"{client_id}:{client_secret}".encode()).decode()
   # Генерация уникального идентификатора запроса
   rq_uid = str(uuid.uuid4())  
   # Заголовки запроса
   headers = {
      'Content-Type': 'application/x-www-form-urlencoded',
      'Accept': 'application/json',
      'Authorization': f'Basic {auth_key}',
      'RqUID': rq_uid
   }
   # Параметры запроса
   data = {
      'scope': 'GIGACHAT_API_PERS',
   }
   # Отправка запроса
   response = requests.post(url, headers=headers, data=data)
   # Проверка на ошибки
   if response.status_code != 200:
      raise Exception(f"Error getting access token: {response.json()}")
   # Возвращаем access token
   return response.json()["access_token"]