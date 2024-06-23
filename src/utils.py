from bs4 import BeautifulSoup
from requests import RequestException

from constants import TEXTS
from exceptions import ParserFindTagException


def get_response(session, url, encoding='utf-8'):
    try:
        response = session.get(url)
        response.encoding = encoding
        return response
    except RequestException as error:
        raise RequestException(
            TEXTS.response_error.format(url, error)
        )


def find_tag(soup, tag, attrs=None):
    searched_tag = soup.find(tag, attrs=(attrs or {}))
    if searched_tag is None:
        raise ParserFindTagException(TEXTS.tag_not_found.format(tag, attrs))
    return searched_tag


def get_soup(session, url, features='lxml'):
    return BeautifulSoup(
        get_response(session, url).text,
        features=features
    )
