# Проект парсинга pep
Простой парсер, предназначенный для получения информации с сайта https://python.org. 
В частности:
- предоставить ссылки на страницы изменений в разных версиях Python;
- предоставить ссылки на документации по версиям Python;
- загрузить документацию в формате pdf для актуальной версии Python;
- сформировать отчет по документам PEP(_Python Enhancement Proposal_).

## Технологии
- [**Python**](https://docs.python.org/3.12/)
- [**requests-cache**](https://pypi.org/project/requests-cache/1.0.0/)
- [**tqdm**](https://pypi.org/project/tqdm/4.66.4/)
- [**beautifulsoup4**](https://pypi.org/project/beautifulsoup4/4.12.3/)
- [**lxml**](https://pypi.org/project/lxml/5.2.2/)
- [**prettytable**](https://pypi.org/project/prettytable/2.1.0/) 

## Использование

### Требования
Для запуска проекта, необходим [Python](https://www.python.org) v3.9+.

### Клонирование проекта
Выполните команду для клонирования и перехода в проект:
```bash
git clone https://github.com/4its/bs4_parser_pep.git && cd bs4_parser_pep
```

### Виртуальное окружение
Для создания и активации окружения:
```bash
python -m venv vevn %% source venv/bin/activate
```

### Установка зависимостей
Для установки зависимостей, выполните команду:
```bash
pip install -r requirements.txt
```

## Команды
Общий формат команд: `python src/main.py [режим работы] [опциональные аргументы]`

#### Вывод справки
```bash
python src/main.py -h
```
Примеры команд:
- Получение списка ссылок на изменения по версиям Python в файле .csv
    ```bash
    ython src/main.py whats-new -o file
    ```
- Получение списка ссылок на изменения по версиям Python в консоль(PrettyPrint)
    ```bash
    ython src/main.py whats-new -o pretty
    ```
- Получение списка ссылок на изменения по версиям Python в консоль(PrettyPrint) _без использования кеширования_:
    ```bash
    ython src/main.py whats-new -с -o pretty
    ```
- Получение статистики документам PEP c выводом в консоль:
    ```bash
    ython src/main.py pep
    ```

### Зачем разработали этот проект?
Данный проект разработан в рамках финального задания по спринту "Парсинг" в [Яндекс.Практикум](https://practicum.yandex.ru/python-developer-plus/)

## Разработчик проекта

- [**Georgii Egiazarian**](https://github.com/4its)
 