#!/usr/bin/env python3

"""Export your Microsoft SQL Server database to CSV."""

import csv
import json
import argparse

from typing import Dict, List, Any

import pyodbc


def get_curr(credentials):
    """Returns a cursor to the database."""
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

    return conn.cursor()


def get_schemas(curr):
    """Returns an object with the schemas of all tables in the database."""
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
    # Dict[table_path: List[fields]]
    tables: Dict[str, List[str]] = {}
    for row in curr.fetchall():
        table_schema, table_name, field_name, _ = row
        path = f'"{table_schema}"."{table_name}"'
        try:
            tables[path].append(field_name)
        except KeyError:
            tables[path] = [field_name]
    return tables


def get_rows(curr, table_path: str, table_fields: List[str]):
    """Return all rows from a table."""
    table_fields_statement = ",".join(table_fields)
    curr.execute(
        f"""
        SELECT
            {table_fields_statement}
        FROM
            {table_path}
        """)
    table_rows = curr.fetchall()
    return table_rows


def print_csv(
        output_dir: str,
        table_path: str,
        table_fields: List[str],
        table_rows) -> None:
    """Prints a table as CSV to stdout."""
    table_path = table_path.replace('"', "")
    file_name = f"{output_dir}/{table_path}.csv"

    with open(file_name, "w") as csvfile:
        writer = csv.writer(
            csvfile,
            delimiter=",",
            quotechar='"',
            quoting=csv.QUOTE_NONNUMERIC)

        writer.writerow(table_fields)
        for row in table_rows:
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
        description="Persists a singer formatted stream to Amazon Redsfhit")
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

    curr = get_curr(credentials)

    print("INFO: gathering schemas...", end=" ", flush=True)
    tables = get_schemas(curr)
    print(f"{len(tables.items())} found.", flush=True)
    print("INFO: processing:", flush=True)
    for table_path, table_fields in tables.items():
        print(f"        {table_path}.", flush=True)
        table_rows = get_rows(curr, table_path, table_fields)
        print_csv(args.output_dir, table_path, table_fields, table_rows)


if __name__ == "__main__":
    main()
