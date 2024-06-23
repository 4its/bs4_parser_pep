import argparse
import logging
from logging.handlers import RotatingFileHandler

from constants import Choices, Logs, Texts

LOG_FORMAT = '%(asctime)s - [%(levelname)s] - %(message)s'
DT_FORMAT = '%d.%m.%Y %H:%M:%S'


def configure_argument_parser(available_modes):
    parser = argparse.ArgumentParser(description=Texts.PARSER_DESCRIPTION)
    parser.add_argument(
        'mode',
        choices=available_modes,
        help=Texts.PARSER_MODE
    )
    parser.add_argument(
        '-c',
        '--clear-cache',
        action='store_true',
        help=Texts.PARSER_CACHE_CLEAN
    )
    parser.add_argument(
        '-o',
        '--output',
        choices=(Choices.PRETTY, Choices.FILE,),
        help=Texts.PARSER_OUTPUTS
    )
    return parser


def configure_logging():
    Logs.DIRECTORY.mkdir(exist_ok=True)
    rotating_handler = RotatingFileHandler(
        Logs.FILE_PATH, maxBytes=10 ** 6, backupCount=5
    )
    logging.basicConfig(
        datefmt=DT_FORMAT,
        format=LOG_FORMAT,
        level=logging.INFO,
        handlers=(rotating_handler, logging.StreamHandler())
    )
