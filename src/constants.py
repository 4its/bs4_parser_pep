from pathlib import Path
from urllib.parse import urljoin


BASE_DIR = Path(__file__).parent
MAIN_DOC_URL = 'https://docs.python.org/3/'
MAIN_PEP_URL = 'https://peps.python.org/'

TQDM_NCOLS = 100


class Choices:
    PRETTY = 'pretty'
    FILE = 'file'


class Dirs:
    DOWNLOADS = 'downloads'
    RESULTS = 'results'


class Logs:
    DIRECTORY = BASE_DIR / 'logs'
    FILENAME = 'parser.log'
    FILE_PATH = DIRECTORY / FILENAME


class Urls:
    DOWNLOAD = urljoin(MAIN_DOC_URL, 'download.html')
    WHATS_NEW = urljoin(MAIN_DOC_URL, 'whatsnew/')


class Texts:
    START_PARSE = 'Парсер запущен!'
    FINISH_PARSE = 'Парсер завершил работу.'
    COMMAND_ARGS = 'Аргументы командной строки: {}'
    FILE_RESULT = 'Файл с результатами был сохранён: {}'
    TAG_NOT_FOUND = 'Не найден тег {} {}'
    RESPONSE_ERROR = 'Ошибка при загрузке страницы {}. Подробности: {}'
    PARSER_DESCRIPTION = 'Парсер документации Python'
    PARSER_MODE = 'Режимы работы парсера'
    PARSER_CACHE_CLEAN = 'Очистка кеша'
    PARSER_OUTPUTS = 'Дополнительные способы вывода данных'
    STATUS_NOT_MATCH = (
        'Несовпадающие статусы: {} Статус в карточке: {} Ожидаемые статусы: {}'
    )
    TQDM_DESCRIPTION = 'Парсим список PEP'
    LOAD_ARCHIVE = 'Архив был загружен и сохранён: {}'
    EXCEPTION = 'Ошибка в работе программы: {}'


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
