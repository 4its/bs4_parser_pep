import logging
import re
from urllib.parse import urljoin

import requests_cache
from tqdm import tqdm

from configs import configure_argument_parser, configure_logging
from constants import BASE_DIR, MAIN_DOC_URL, MAIN_PEP_URL, EXPECTED_STATUS
from outputs import control_output
from utils import get_soup, find_tag


def whats_new(session):
    whats_new_url = urljoin(MAIN_DOC_URL, 'whatsnew/')
    soup = get_soup(session, whats_new_url)
    main_div = find_tag(soup, 'section', attrs={'id': 'what-s-new-in-python'})
    div_with_ul = find_tag(main_div, 'div', attrs={'class': 'toctree-wrapper'})
    sections_by_python = div_with_ul.find_all(
        'li', attrs={'class': 'toctree-l1'}
    )
    results = [('Ссылка на статью', 'Заголовок', 'Редактор, автор')]
    for section in tqdm(sections_by_python):
        version_a_tag = section.find('a')
        href = version_a_tag['href']
        version_link = urljoin(whats_new_url, href)
        soup = get_soup(session, version_link)
        h1 = find_tag(soup, 'h1')
        dl = find_tag(soup, 'dl')
        dl_text = dl.text.replace('\n', ' ')
        results.append((version_link, h1.text, dl_text))
    return results


def latest_versions(session):
    soup = get_soup(session, MAIN_DOC_URL)
    sidebar = find_tag(soup, 'div', {'class': 'sphinxsidebar'})
    ul_tags = sidebar.find_all('ul')
    for ul in ul_tags:
        if 'All versions' in ul.text:
            a_tags = ul.find_all('a')
            break
    else:
        raise Exception('Ничего не нашлось')
    results = [('Ссылка на документацию', 'Версия', 'Статус')]
    pattern = r'Python (?P<version>\d\.\d+) \((?P<status>.*)\)'
    for a_tag in a_tags:
        link = a_tag['href']
        text_match = re.search(pattern, a_tag.text)
        if text_match:
            version, status = text_match.groups()
        else:
            version, status = a_tag.text, ''
        results.append((link, version, status))
    return results


def download(session):
    downloads_url = urljoin(MAIN_DOC_URL, 'download.html')
    pattern = r'.+pdf-a4\.zip$'
    soup = get_soup(session, downloads_url)
    table = find_tag(soup, 'table', {'class': 'docutils'})
    pdf_a4_tag = find_tag(table, 'a', {'href': re.compile(pattern)})
    pdf_a4_link = pdf_a4_tag['href']
    archive_url = urljoin(downloads_url, pdf_a4_link)
    filename = archive_url.split('/')[-1]
    downloads_dir = BASE_DIR / 'downloads'
    downloads_dir.mkdir(exist_ok=True)
    archive_path = downloads_dir / filename
    response = session.get(archive_url)
    with open(archive_path, 'wb') as file:
        file.write(response.content)
    logging.info(f'Архив был загружен и сохранён: {archive_path}')


def pep(session):
    soup = get_soup(session, MAIN_PEP_URL)
    section_table = find_tag(soup, 'section', {'id': 'numerical-index'})
    tbody = find_tag(section_table, 'tbody')
    pep_list = tbody.find_all('tr')
    results = [('Статус', 'Количество')]
    pep_count = 0
    status_sums = {}
    for pep in tqdm(pep_list, desc='Парсим список PEP'):
        pep_count += 1
        status_preview = pep.find('abbr').text
        if len(status_preview) > 1:
            status_preview = status_preview[1:]
        else:
            status_preview = ''
        pep_link = urljoin(MAIN_PEP_URL, pep.find('a')['href'])
        table = find_tag(
            get_soup(session, pep_link),
            'dl',
            {'class': 'rfc2822 field-list simple'}
        )
        status_page = table.find(
            string='Status'
        ).parent.find_next_sibling('dd').string
        if status_page in status_sums:
            status_sums[status_page] += 1
        if status_page not in status_sums:
            status_sums[status_page] = 1
        if status_page not in EXPECTED_STATUS[status_preview]:
            message = (
                'Несовпадающие статусы:'
                f' {pep_link}'
                f' Статус в карточке: {status_page}'
                f' Ожидаемые статусы: {EXPECTED_STATUS[status_preview]}'
            )
            logging.warning(message)
    results += [(status, status_sums[status]) for status in status_sums]
    results.append(('Total', pep_count))
    return results


MODE_TO_FUNCTION = {
    'whats-new': whats_new,
    'latest-versions': latest_versions,
    'download': download,
    'pep': pep,
}


def main():
    configure_logging()
    logging.info('Парсер запущен!')
    arg_parser = configure_argument_parser(MODE_TO_FUNCTION.keys())
    args = arg_parser.parse_args()
    logging.info(f'Аргументы коммандной строки: {args}')
    session = requests_cache.CachedSession()
    if args.clear_cache:
        session.cache.clear()
    parser_mode = args.mode
    results = MODE_TO_FUNCTION[parser_mode](session)
    if results is not None:
        control_output(results, args)
    logging.info('Парсер завершил работу.')


if __name__ == '__main__':
    main()
