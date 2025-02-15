import logging
import re
from collections import defaultdict
from urllib.parse import urljoin

import requests_cache
from tqdm import tqdm

from configs import configure_argument_parser, configure_logging
from constants import (
    BASE_DIR, Dirs, EXPECTED_STATUS, MAIN_DOC_URL, MAIN_PEP_URL,
    Texts, TQDM_NCOLS, Urls
)
from outputs import control_output
from utils import find_tag, get_soup


def whats_new(session):
    results = []
    errors = []
    for link in tqdm(
        get_soup(session, Urls.WHATS_NEW).select(
            '#what-s-new-in-python div.toctree-wrapper'
            ' li.toctree-l1 a[href$=".html"]'
        ),
        ncols=TQDM_NCOLS
    ):
        version_link = urljoin(Urls.WHATS_NEW, link['href'])
        try:
            soup = get_soup(session, version_link)
            results.append(
                (
                    version_link,
                    find_tag(soup, 'h1').text,
                    find_tag(soup, 'dl').text.replace('\n', ' ')
                )
            )
        except ConnectionError as error:
            errors.append(Texts.RESPONSE_ERROR.format(version_link, error))
    [*map(logging.error, errors)]
    return [
        ('Ссылка на статью', 'Заголовок', 'Редактор, автор'),
        *results
    ]


def latest_versions(session):
    soup = get_soup(session, MAIN_DOC_URL)
    sidebar = find_tag(soup, 'div', {'class': 'sphinxsidebar'})
    ul_tags = sidebar.find_all('ul')
    for ul in ul_tags:
        if 'All versions' in ul.text:
            a_tags = ul.find_all('a')
            break
    else:
        raise LookupError(Texts.NOTHING_FOUND)
    results = []
    pattern = r'Python (?P<version>\d\.\d+) \((?P<status>.*)\)'
    for a_tag in a_tags:
        text_match = re.search(pattern, a_tag.text)
        if text_match:
            version, status = text_match.groups()
        else:
            version, status = a_tag.text, ''
        results.append((a_tag['href'], version, status))
    return [
        ('Ссылка на документацию', 'Версия', 'Статус'),
        *results,
    ]


def download(session):
    archive_url = urljoin(
        Urls.DOWNLOAD,
        get_soup(session, Urls.DOWNLOAD).select_one(
            'table.docutils a[href$="pdf-a4.zip"]'
        )['href']
    )
    downloads_dir = BASE_DIR / Dirs.DOWNLOADS
    downloads_dir.mkdir(exist_ok=True)
    archive_path = downloads_dir / archive_url.split('/')[-1]
    response = session.get(archive_url)
    with open(archive_path, 'wb') as file:
        file.write(response.content)
    logging.info(Texts.LOAD_ARCHIVE.format(archive_path))


def pep(session):
    soup = get_soup(session, MAIN_PEP_URL)
    section_table = find_tag(soup, 'section', {'id': 'numerical-index'})
    tbody = find_tag(section_table, 'tbody')
    pep_list = tbody.find_all('tr')
    status_sums = defaultdict(int)
    errors = []
    warnings = []
    for pep in tqdm(pep_list, desc=Texts.TQDM_DESCRIPTION, ncols=TQDM_NCOLS):
        status_preview = pep.find('abbr').text
        status_preview = status_preview[1:] if len(status_preview) > 1 else ''
        pep_link = urljoin(MAIN_PEP_URL, pep.find('a')['href'])
        try:
            table = find_tag(
                get_soup(session, pep_link),
                'dl',
                {'class': 'rfc2822 field-list simple'}
            )
            status_page = table.find(
                string='Status'
            ).parent.find_next_sibling('dd').string
            status_sums[status_page] += 1
            if status_page not in EXPECTED_STATUS[status_preview]:
                warnings.append(
                    Texts.STATUS_NOT_MATCH.format(
                        pep_link,
                        status_page,
                        EXPECTED_STATUS[status_preview]
                    )
                )
        except ConnectionError as error:
            errors.append(Texts.RESPONSE_ERROR.format(pep_link, error))
    [*map(logging.error, errors)]
    [*map(logging.warning, warnings)]
    return [
        ('Статус', 'Количество'),
        *status_sums.items(),
        ('Всего', sum(status_sums.values())),
    ]


MODE_TO_FUNCTION = {
    'whats-new': whats_new,
    'latest-versions': latest_versions,
    'download': download,
    'pep': pep,
}


def main():
    configure_logging()
    logging.info(Texts.START_PARSE)
    arg_parser = configure_argument_parser(MODE_TO_FUNCTION.keys())
    args = arg_parser.parse_args()
    logging.info(Texts.COMMAND_ARGS.format(args))
    try:
        session = requests_cache.CachedSession()
        if args.clear_cache:
            session.cache.clear()
        parser_mode = args.mode
        results = MODE_TO_FUNCTION[parser_mode](session)
        if results is not None:
            control_output(results, args)
    except Exception as e:
        logging.exception(Texts.ERROR_WHEN_RUN.format(e))
    logging.info(Texts.FINISH_PARSE)


if __name__ == '__main__':
    main()
