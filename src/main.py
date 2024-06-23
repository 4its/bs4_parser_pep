from collections import defaultdict
import logging
import re
from urllib.parse import urljoin

import requests_cache
from tqdm import tqdm

from configs import configure_argument_parser, configure_logging
from constants import (
    BASE_DIR, MAIN_DOC_URL, MAIN_PEP_URL, EXPECTED_STATUS, DIRS, TEXTS, URLS
)
from outputs import control_output
from utils import get_soup, find_tag


def whats_new(session):
    sections_by_python = get_soup(session, URLS.whats_new).select(
        '#what-s-new-in-python div.toctree-wrapper li.toctree-l1'
    )
    results = []
    for section in tqdm(sections_by_python):
        version_a_tag = section.find('a')
        href = version_a_tag['href']
        version_link = urljoin(URLS.whats_new, href)
        soup = get_soup(session, version_link)
        results.append(
            (
                version_link,
                find_tag(soup, 'h1').text,
                find_tag(soup, 'dl').text.replace('\n', ' ')
            )
        )
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
        raise ValueError('Ничего не нашлось')
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
        URLS.download,
        get_soup(session, URLS.download).select_one(
            'table.docutils a[href$="pdf-a4.zip"]'
        )['href']
    )
    downloads_dir = BASE_DIR / DIRS.downloads
    downloads_dir.mkdir(exist_ok=True)
    archive_path = downloads_dir / archive_url.split('/')[-1]
    response = session.get(archive_url)
    with open(archive_path, 'wb') as file:
        file.write(response.content)
    logging.info(TEXTS.load_archive.format(archive_path))


def pep(session):
    soup = get_soup(session, MAIN_PEP_URL)
    section_table = find_tag(soup, 'section', {'id': 'numerical-index'})
    tbody = find_tag(section_table, 'tbody')
    pep_list = tbody.find_all('tr')
    status_sums = defaultdict(int)
    warnings = []
    for pep in tqdm(pep_list, desc=TEXTS.tqdm_description):
        status_preview = pep.find('abbr').text
        status_preview = status_preview[1:] if len(status_preview) > 1 else ''
        pep_link = urljoin(MAIN_PEP_URL, pep.find('a')['href'])
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
                TEXTS.status_not_match.format(
                    pep_link,
                    status_page,
                    EXPECTED_STATUS[status_preview]
                )
            )
    if warnings:
        for warning in warnings:
            logging.warning(warnings)
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
    logging.info(TEXTS.start_parse)
    arg_parser = configure_argument_parser(MODE_TO_FUNCTION.keys())
    args = arg_parser.parse_args()
    logging.info(TEXTS.command_args.format(args))
    try:
        session = requests_cache.CachedSession()
        if args.clear_cache:
            session.cache.clear()
        parser_mode = args.mode
        results = MODE_TO_FUNCTION[parser_mode](session)
        if results is not None:
            control_output(results, args)
    except Exception as e:
        logging.error(e)
    logging.info(TEXTS.finish_parse)


if __name__ == '__main__':
    main()
