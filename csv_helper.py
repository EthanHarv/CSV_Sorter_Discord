'''
Helper functions for reading, sorting, and writing csv files
'''


import csv
from empty_error import FileEmptyError

def read_csv(filename: str) -> list[list[str]]:
    '''
    Accepts a csv filename, reads content, and returns the sorted list of rows.

    :param file: Filename to read from
    :return: 2d list of strings (list of rows)

    :raises FileNotFoundError: File not found
    :raises PermissionError: Program lacks permission to read file
    '''

    try:
        with open(filename, encoding='utf-8', mode='r') as file:
            reader = csv.reader(file)
            rows = []
            for row in reader:
                rows.append(row)
            return rows
    except FileNotFoundError as err:
        raise err
    except PermissionError as err:
        raise err


def sort_csv(rows: list[list[str]]) -> list[list[str]]:
    '''
    Accepts a list of csv rows, reads content, and returns the sorted list of rows (with first row of headers fixed).

    Always sorts by the content of the first column, numerically.

    :param file: Filename to read from
    :return: 2d list of strings (list of rows)

    :raises ValueError: Column contains non-numeric values.
    :raises FileEmptyError: File contains no rows.
    '''

    rows = rows.copy()

    if len(rows) == 0:
        raise FileEmptyError('Input file is empty')

    # In [brackets] to maintain list structure for later
    first = [rows.pop(0)]

    # Sort by first column
    try:
        sorted_rows = sorted(rows, key = lambda row: float(row[0]))
    except ValueError as err:
        raise err

    return first + sorted_rows


def write_csv(filename: str, rows: list[list[str]]) -> None:
    '''
    Takes a filename and a list of rows, and attempts to write the csv out.

    :param file: Filename to write to
    :param rows: A list of rows

    :raises PermissionError: Program lacks permission to write file
    '''

    try:
        with open(filename, encoding='utf-8', mode='w', newline='') as file:
            writer = csv.writer(file)
            for row in rows:
                writer.writerow(row)
    except PermissionError as err:
        raise err
