import argparse
import logging
from logging.handlers import RotatingFileHandler

from constants import BASE_DIR, MESSAGES

LOG_FORMAT = '%(asctime)s - [%(levelname)s] - %(message)s'
DT_FORMAT = '%d.%m.%Y %H:%M:%S'


def configure_argument_parser(available_modes):
    parser = argparse.ArgumentParser(description=MESSAGES.parser_description)
    parser.add_argument(
        'mode',
        choices=available_modes,
        help=MESSAGES.parser_mode
    )
    parser.add_argument(
        '-c',
        '--clear-cache',
        action='store_true',
        help=MESSAGES.parser_cache_clean
    )
    parser.add_argument(
        '-o',
        '--output',
        choices=('pretty', 'file'),
        help=MESSAGES.parser_outputs
    )
    return parser


def configure_logging():
    log_dir = BASE_DIR / 'logs'
    log_dir.mkdir(exist_ok=True)
    log_file = log_dir / 'parser.log'
    rotating_handler = RotatingFileHandler(
        log_file, maxBytes=10 ** 6, backupCount=5
    )
    logging.basicConfig(
        datefmt=DT_FORMAT,
        format=LOG_FORMAT,
        level=logging.INFO,
        handlers=(rotating_handler, logging.StreamHandler())
    )
