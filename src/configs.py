import argparse
import logging
from logging.handlers import RotatingFileHandler

from constants import LOGS, TEXTS

LOG_FORMAT = '%(asctime)s - [%(levelname)s] - %(message)s'
DT_FORMAT = '%d.%m.%Y %H:%M:%S'


def configure_argument_parser(available_modes):
    parser = argparse.ArgumentParser(description=TEXTS.parser_description)
    parser.add_argument(
        'mode',
        choices=available_modes,
        help=TEXTS.parser_mode
    )
    parser.add_argument(
        '-c',
        '--clear-cache',
        action='store_true',
        help=TEXTS.parser_cache_clean
    )
    parser.add_argument(
        '-o',
        '--output',
        choices=('pretty', 'file'),
        help=TEXTS.parser_outputs
    )
    return parser


def configure_logging():
    LOGS.directory.mkdir(exist_ok=True)
    rotating_handler = RotatingFileHandler(
        LOGS.file_path, maxBytes=10 ** 6, backupCount=5
    )
    logging.basicConfig(
        datefmt=DT_FORMAT,
        format=LOG_FORMAT,
        level=logging.INFO,
        handlers=(rotating_handler, logging.StreamHandler())
    )
