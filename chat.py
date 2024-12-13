from starlette.applications import Starlette
from starlette.responses import HTMLResponse, JSONResponse
from starlette.routing import Route
from starlette.middleware.cors import CORSMiddleware
from llm import get_answer
from news import fetch_and_parse_news
import re


# Простая логика чат-бота с улучшенным форматированием
def bot_logic(user_message: str) -> str:
    if "привет" in user_message.lower():
        return ("Привет! Добро пожаловать в"
                "информационный сервис ЧелГУ! Как я могу помочь?")
    else:
        response = get_answer(user_message)
        # Разбиение длинных текстов на абзацы или разделение на части
        formatted_response = format_response(response)
        return formatted_response


def format_response(response: str) -> str:
    """
    Форматирует строку ответа:
    - Убирает точку в конце ссылки, если она есть.
    - Преобразует ссылки в HTML-формат <a>.
    - Разделяет текст на абзацы.
    """
    # Убираем точку только в конце ссылки
    response = re.sub(r'(https?://[^\s]+)\.$', r'\1', response)

    # Заменяем ссылки на HTML-теги <a>
    formatted_text = re.sub(
        r'(https?://[^\s]+)',
        r'<a href="\1" target="_blank">Ссылка</a>',
        response
    )

    # Разделяем текст на абзацы
    paragraphs = formatted_text.split("\n")
    formatted_text = "".join(
        f"<p>{paragraph.strip()}</p>\n"
        for paragraph in paragraphs if paragraph.strip()
    )

    return formatted_text


# Эндпоинт для обработки сообщений
async def chatbot_endpoint(request):
    data = await request.json()
    user_message = data.get("message")

    if not user_message:
        return JSONResponse({"error": "Message is required"}, status_code=400)

    bot_response = bot_logic(user_message)
    return JSONResponse({"response": bot_response})


# Эндпоинт для получения новостей
async def get_news_endpoint(request):
    # Получаем новости
    news = fetch_and_parse_news()

    if news:
        formatted_news = []
        for item in news:
            title = item.get("Заголовок", "Заголовок не найден")
            link = item.get("Ссылка", "#")
            date = item.get("Дата", "Дата не указана")

            # Форматируем новость
            formatted_news.append({
                "title": title,
                "date": date,
                "link": link
            })

        return JSONResponse({"news": formatted_news})
    else:
        return JSONResponse({"error": "Не удалось получить новости"},
                            status_code=500)


# Эндпоинт для отображения интерфейса
async def index(request):
    with open('interface.html', 'r', encoding='utf-8') as file:
        html_content = file.read()
    return HTMLResponse(html_content)

# Определение маршрутов
routes = [
    Route("/", index),
    Route("/chat", chatbot_endpoint, methods=["POST"]),
    Route("/news", get_news_endpoint),
]

# Инициализация приложения Starlette
app = Starlette(debug=True, routes=routes)

# Разрешение CORS (опционально, если требуется доступ с других доменов)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
