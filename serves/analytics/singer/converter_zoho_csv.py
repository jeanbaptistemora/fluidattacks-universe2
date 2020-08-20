#! /usr/bin/env python3

# Standard imports
import os
import csv
import sys
import argparse
import contextlib
import urllib.parse

# Third parties imports
import requests


def export_csv(
        target: str,
        email: str, token: str,
        space: str, table: str) -> bool:
    """Export a Zoho Table from a Workspace to a CSV."""
    # pylint: disable=too-many-locals
    email = urllib.parse.quote(email)
    token = urllib.parse.quote(token)
    table = urllib.parse.quote(table)
    space = urllib.parse.quote(space)

    with requests.Session() as session:
        request = requests.Request(
            method='POST',
            url=f'https://analyticsapi.zoho.com/api/{email}/{space}/{table}',
            params={
                'authtoken': token,
                'ZOHO_ACTION': 'EXPORT',
                'ZOHO_OUTPUT_FORMAT': 'CSV',
                'ZOHO_ERROR_FORMAT': 'JSON',
                'ZOHO_API_VERSION': '1.0',
            })
        response = session.send(
            request=request.prepare(),
            stream=True)

        with open(f'_{target}', 'wb') as target_handle:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    target_handle.write(chunk)

        # Open and save again to re-format the CSV with QUOTE_NONNUMERIC
        with open(f'_{target}') as source, open(target, 'w') as dest:
            source_reader = csv.DictReader(source)
            dest_writer = csv.DictWriter(
                f=dest,
                fieldnames=source_reader.fieldnames,
                quoting=csv.QUOTE_NONNUMERIC)
            dest_writer.writeheader()
            for row in source_reader:
                for column in row:
                    # Transform the string into a proper numeric type
                    with contextlib.suppress(ValueError):
                        val_int: int = int(row[column])
                        val_float: float = round(float(row[column]), 6)
                        row[column] = (
                            val_int  # type: ignore
                            if val_int == val_float
                            else val_float)
                dest_writer.writerow(row)

        os.unlink(f'_{target}')

    return True


def cli():
    """Usual entrypoint."""
    parser = argparse.ArgumentParser()
    parser.add_argument('--email', required=True)
    parser.add_argument('--token', required=True)
    parser.add_argument('--space', required=True)
    parser.add_argument('--table', required=True)
    parser.add_argument('--target', required=True)
    args = parser.parse_args()

    success: bool = export_csv(
        target=args.target,
        email=args.email, token=args.token,
        space=args.space, table=args.table)

    sys.exit(0 if success else 1)


if __name__ == '__main__':
    cli()
