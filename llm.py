import requests
import uuid
import json
import os
from dotenv import load_dotenv


load_dotenv()


# Получение токена авторизации для GigaChat API
def get_token(auth_token, scope='GIGACHAT_API_PERS'):
    """
    Выполняет POST-запрос для получения токена авторизации.

    :param auth_token: Токен авторизации.
    :param scope: Область действия токена. По умолчанию 'GIGACHAT_API_PERS'.
    :return: Токен доступа или None в случае ошибки.
    """
    rq_uid = str(uuid.uuid4())
    url = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'application/json',
        'RqUID': rq_uid,
        'Authorization': f'Basic {auth_token}'
    }
    payload = {'scope': scope}

    try:
        response = requests.post(url,
                                 headers=headers,
                                 data=payload,
                                 verify=False)
        response.raise_for_status()
        return response.json().get('access_token')
    except requests.RequestException as e:
        print(f"Ошибка при получении токена: {str(e)}")
        return None


# Общение с GigaChat API
def get_chat_completion(auth_token, user_message, conversation_history=None):
    """
    Отправляет сообщение пользователю и возвращает ответ от GigaChat.

    :param auth_token: Токен авторизации.
    :param user_message: Сообщение пользователя.
    :param conversation_history: История диалога.
    :return: Ответ от GigaChat или None в случае ошибки.
    """
    url = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"

    if conversation_history is None:
        conversation_history = []

    conversation_history.append({"role": "user", "content": user_message})
    payload = json.dumps({
        "model": "GigaChat:latest",
        "messages": conversation_history,
        "temperature": 1,
        "top_p": 0.1,
        "n": 1,
        "stream": False,
        "max_tokens": 512,
        "repetition_penalty": 1,
        "update_interval": 0
    })

    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'Bearer {auth_token}'
    }

    try:
        response = requests.post(url,
                                 headers=headers,
                                 data=payload,
                                 verify=False)
        response.raise_for_status()
        response_data = response.json()
        model_response = response_data['choices'][0]['message']['content']
        conversation_history.append({"role": "assistant",
                                     "content": model_response})
        return model_response
    except requests.RequestException as e:
        print(f"Ошибка при общении с GigaChat: {str(e)}")
        return None


# Основная функция для получения ответа пользователя
def get_answer(user_message):
    """
    Функция для получения ответа на сообщение пользователя.

    :param user_message: Сообщение пользователя.
    :return: Ответ для пользователя.
    """
    sber_auth = os.getenv("sber_auth")
    google_key = os.getenv("google_key")
    engine_api = os.getenv("engine_api")

    giga_token = get_token(sber_auth)
    if not giga_token:
        print("Не удалось получить токен.")
        return "Ошибка авторизации."

    search_url = 'https://www.googleapis.com/customsearch/v1'
    search_params = {
        'q': user_message,  # Используем сообщение пользователя для запроса
        'key': google_key,
        'cx': engine_api
    }

    try:
        search_response = requests.get(search_url, params=search_params)
        search_response.raise_for_status()
        search_results = search_response.json()
        link = search_results['items'][0]['link']
    except Exception as e:
        print(f"Ошибка при поиске ссылки: {str(e)}")
        link = ""
    print("LINK", link)
    # Формируем историю диалога с начальным сообщением
    initial_message = (
        f"Ты информационный сервис ЧелГУ. ТВОЙ ОТВЕТ НЕ ОЧЕНЬ ДЛИННЫЙ. "
        f"ОБЯЗАТЕЛЬНО скажи, что всю информацию можно найти по ссылке "
        f"и ПРИШЛИ ЕМУ эти ССЫЛКИ {link}."
    )
    print(initial_message)
    conversation_history = [{"role": "system", "content": initial_message}]

    response = get_chat_completion(giga_token,
                                   user_message,
                                   conversation_history)

    if response:
        return response
    return "Ошибка при получении ответа от GigaChat."
