#!/usr/bin/env python3

"""Export your Microsoft SQL Server database to CSV with (almost) no RAM.

Your database must be able to handle at least two simultaneous connections.
"""

import csv
import json
import argparse

from typing import List, Any
from contextlib import contextmanager

import pyodbc


@contextmanager
def get_cursor(credentials):
    """Returns a safe cursor to the database."""
    driver = credentials["DRIVER"]
    server = credentials["SERVER"]
    database = credentials["DATABASE"]
    uid = credentials["UID"]
    pwd = credentials["PWD"]

    conn = pyodbc.connect((
        f"DRIVER={driver};"
        f"SERVER={server};"
        f"DATABASE={database};"
        f"UID={uid};"
        f"PWD={pwd};"))

    curr = conn.cursor()

    try:
        yield curr
    finally:
        curr.close()
        conn.close()


def iter_tables(credentials):
    """Yield (table_path, table_fields) for all schema[i].table[j]."""
    with get_cursor(credentials) as curr:
        curr.execute(
            """
            SELECT
                TABLE_SCHEMA, TABLE_NAME, COLUMN_NAME, ORDINAL_POSITION
            FROM
                INFORMATION_SCHEMA.COLUMNS
            ORDER BY
                TABLE_SCHEMA ASC,
                TABLE_NAME ASC,
                ORDINAL_POSITION ASC,
                COLUMN_NAME ASC
            """)
        initial_cycle = True
        current_table_path: str = ""
        table_fields: List[str] = []
        for table_schema, table_name, field_name, _ in curr:
            table_path = f'"{table_schema}"."{table_name}"'
            if current_table_path == table_path:
                table_fields.append(field_name)
            elif initial_cycle:
                initial_cycle = False
            else:
                yield (current_table_path, table_fields)
                table_fields = [field_name]
            current_table_path = table_path


def iter_rows(credentials, table_path: str, table_fields: List[str]):
    """Yield rows from a table."""
    table_fields_statement = ",".join(table_fields)
    with get_cursor(credentials) as curr:
        curr.execute(
            f"""
            SELECT
                {table_fields_statement}
            FROM
                {table_path}
            """)
        for row in curr:
            yield row


def write_csv(
        credentials,
        output_dir: str,
        table_path: str,
        table_fields: List[str]) -> None:
    """Prints a table as CSV to stdout."""
    csv_name = table_path.replace('"', "").replace('.', "__")
    file_name = f"{output_dir}/{csv_name}.csv"

    print(f"writing csv from {table_path} to {file_name}.", flush=True)

    with open(file_name, "w") as csvfile:
        writer = csv.writer(
            csvfile,
            delimiter=",",
            quotechar='"',
            quoting=csv.QUOTE_NONNUMERIC)

        writer.writerow(table_fields)
        for row in iter_rows(credentials, table_path, table_fields):
            casted_row = []
            for value in row:
                value_ascsv: Any = ""
                value_type = type(value).__name__
                if value_type == "str":
                    value_ascsv = value
                elif value_type in ("int", "float", "Decimal", ):
                    value_ascsv = float(value)
                elif value_type == "datetime":
                    value_ascsv = value.strftime('%Y-%m-%dT%H:%M:%SZ')
                elif value_type == "NoneType":
                    pass
                else:
                    value_ascsv = repr(value)
                casted_row.append(value_ascsv)
            writer.writerow(casted_row)


def main():
    """Usual entry point."""
    parser = argparse.ArgumentParser(
        description="Export your entire database to CSV files.")
    parser.add_argument(
        "-a", "--auth",
        required=True,
        help="JSON authentication file",
        type=argparse.FileType("r"),
        dest="auth")
    parser.add_argument(
        "-o", "--output-dir",
        required=True,
        help="path to write",
        dest="output_dir")
    args = parser.parse_args()

    credentials = json.load(args.auth)

    for table_path, table_fields in iter_tables(credentials):
        write_csv(credentials, args.output_dir, table_path, table_fields)


if __name__ == "__main__":
    main()
