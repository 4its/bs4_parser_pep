import csv
import datetime as dt
import logging

from prettytable import PrettyTable

from constants import BASE_DIR, CHOICES, DATETIME_FORMAT, DIRS, TEXTS


def control_output(results, cli_args):
    output_choices = {
        CHOICES.pretty: pretty_output,
        CHOICES.file: file_output,
    }
    if cli_args.output in output_choices:
        output_choices[cli_args.output](results, cli_args)
    else:
        default_output(results)


def default_output(results):
    for row in results:
        print(*row)


def pretty_output(results, *args):
    table = PrettyTable()
    table.field_names = results[0]
    table.align = 'l'
    table.add_rows(results[1:])
    print(table)


def file_output(results, cli_args):
    results_dir = BASE_DIR / DIRS.results
    results_dir.mkdir(exist_ok=True)
    parser_mode = cli_args.mode
    now = dt.datetime.now()
    now_formatted = now.strftime(DATETIME_FORMAT)
    file_name = f'{parser_mode}_{now_formatted}.csv'
    file_path = results_dir / file_name
    with open(file_path, 'w', encoding='utf-8') as file:
        writer = csv.writer(file, dialect=csv.unix_dialect)
        writer.writerows(results)
    logging.info(TEXTS.file_result.format(file_path))
