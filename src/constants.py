from pathlib import Path
from urllib.parse import urljoin


BASE_DIR = Path(__file__).parent
MAIN_DOC_URL = 'https://docs.python.org/3/'
MAIN_PEP_URL = 'https://peps.python.org/'


class CHOICES:
    pretty = 'pretty'
    file = 'file'


class DIRS:
    downloads = 'downloads'
    results = 'results'


class LOGS:
    directory = BASE_DIR / 'logs'
    filename = 'parser.log'
    file_path = directory / filename


class URLS:
    download = urljoin(MAIN_DOC_URL, 'download.html')
    whats_new = urljoin(MAIN_DOC_URL, 'whatsnew/')


class TEXTS:
    start_parse = 'Парсер запущен!'
    finish_parse = 'Парсер завершил работу.'
    command_args = 'Аргументы командной строки: {}'
    file_result = 'Файл с результатами был сохранён: {}'
    tag_not_found = 'Не найден тег {} {}'
    response_error = 'Ошибка при загрузке страницы {}. Подробности: {}'
    parser_description = 'Парсер документации Python'
    parser_mode = 'Режимы работы парсера'
    parser_cache_clean = 'Очистка кеша'
    parser_outputs = 'Дополнительные способы вывода данных'
    status_not_match = (
        'Несовпадающие статусы: {} Статус в карточке: {} Ожидаемые статусы: {}'
    )
    tqdm_description = 'Парсим список PEP'
    load_archive = 'Архив был загружен и сохранён: {}'


DATETIME_FORMAT = '%Y-%m-%d_%H-%M-%S'
EXPECTED_STATUS = {
    'A': ('Active', 'Accepted'),
    'D': ('Deferred',),
    'F': ('Final',),
    'P': ('Provisional',),
    'R': ('Rejected',),
    'S': ('Superseded',),
    'W': ('Withdrawn',),
    '': ('Draft', 'Active'),
}
