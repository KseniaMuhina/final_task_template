import requests
from bs4 import BeautifulSoup


def fetch_and_parse_news():
    """
    Функция для получения и обработки новостей из указанного API URL.
    :return: None
    """
    api_url = (
        "https://www.csu.ru/_api/web/lists/getByTitle('Новости')"
        "/items?$top=3&$orderby=Created desc"
    )
    response = requests.get(api_url)
    news_data = []
    if response.status_code == 200:
        # Парсим XML-ответ
        soup = BeautifulSoup(response.content, 'xml')

        # Ищем все записи новостей
        news_entries = soup.find_all('entry')

        if not news_entries:
            print("Новостей не найдено.")
            return

        # Перебираем и обрабатываем каждую новость
        for idx, entry in enumerate(news_entries, 1):
            title_tag = entry.find('d:Title')
            title = title_tag.text if title_tag else "Без заголовка"

            link_tag = entry.find('d:ID')
            link = link_tag.text if link_tag else "Ссылка отсутствует"

            date_tag = entry.find('d:Created')
            date = date_tag.text if date_tag else "Дата не указана"

            news_data.append({
                "Новость": idx,
                "Заголовок": title,
                "Ссылка": (
                    f"https://www.csu.ru/Lists/List1/newsitem.aspx?ID={link}"
                ),
                "Дата": date
            })

        return news_data
    else:
        return [f"Ошибка при запросе к API: {response.status_code}"]
