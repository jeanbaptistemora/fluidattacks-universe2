#! /usr/bin/env python3

# Standard imports
import sys
import argparse
import urllib.parse

# Third parties imports
import requests


def export_csv(
        target: str,
        email: str, token: str,
        space: str, table: str) -> bool:
    """Export a Zoho Table from a Workspace to a CSV."""
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

        with open(target, 'wb') as target_handle:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    target_handle.write(chunk)

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
