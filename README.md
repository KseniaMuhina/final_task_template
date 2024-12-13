## Запуск сервера

Для запуска приложения используйте команду:

```bash
uvicorn chat:app --reload
```

## Техническое задание (ТЗ)
### Проект: Информационный сервис для ЧелГУ
Обзор проекта:
Разработать текстовый сервис, предоставляющий информацию о Челябинском государственном университете (ЧелГУ). Сервис должен комбинировать общую информацию из моделей LLM (например, GPT-4, Llama) с данными из интернета, такими как новости ЧелГУ и релевантные ссылки.

## Цели проекта:
### Предоставление информации о ЧелГУ:
1. Ответы на вопросы о факультетах, программах, событиях и других аспектах университета.
2. Интеграция с внешними источниками данных:
- Поиск информации о ЧелГУ в интернете и предоставление релевантных ссылок.
- Получение актуальных новостей с сайта ЧелГУ.

### Функциональные требования:
1. Поиск релевантных ссылок:
- Сервис должен выполнять поиск в интернете по запросам, связанным с ЧелГУ, и предоставлять пользователю не более трёх актуальных ссылок.
- Использовать Google Search API или другую поисковую систему для получения данных.
2. Получение новостей с сайта ЧелГУ:
- Сервис должен отображать актуальные новости с официального сайта ЧелГУ.
- Использовать веб-скрапинг (BeautifulSoup) или RSS-фид для извлечения данных.
- Заголовки новостей должны быть лаконичными (до трёх пунктов).
