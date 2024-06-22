import logging

from bs4 import BeautifulSoup
from requests import RequestException

from constants import MESSAGES
from exceptions import ParserFindTagException


def get_response(session, url, encoding='utf-8'):
    try:
        response = session.get(url)
        response.encoding = encoding
        return response
    except RequestException as e:
        logging.exception(
            MESSAGES.response_error.format(url, e),
            stack_info=True,
        )


def find_tag(soup, tag, attrs=None):
    searched_tag = soup.find(tag, attrs=(attrs or {}))
    if searched_tag is None:
        error_message = MESSAGES.tag_not_found.format(tag, attrs)
        logging.error(error_message, stack_info=True)
        raise ParserFindTagException(error_message)
    return searched_tag


def get_soup(session, url, features='lxml'):
    return BeautifulSoup(
        get_response(session, url).text,
        features=features
    )
