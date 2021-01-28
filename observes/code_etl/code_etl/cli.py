# Standard libraries
import asyncio
import sys
from os.path import abspath
from typing import Iterator, Tuple
# Third party libraries
import click
# Local libraries
from code_etl import (
    ammend_authors as ammend,
    compute_bills as bills,
    upload
)


@click.command()
@click.argument('mailmap_path', type=str)
def ammend_authors(mailmap_path: str) -> None:
    asyncio.run(ammend.main(mailmap_path))


@click.command()
@click.argument('folder', type=str)
@click.argument('year', type=int)
@click.argument('month', type=int)
@click.argument('integrates_token', type=str)
def compute_bills(
    folder: str,
    year: int,
    month: int,
    integrates_token: str
) -> None:
    bills.main(
        folder, year, month,
        integrates_token,
    )


@click.command()
@click.argument('namespace', type=str)
@click.argument('repositories', type=str, nargs=-1)
def upload_code(namespace: str, repositories: Tuple[str, ...]) -> None:
    repos: Iterator[str] = map(abspath, repositories)
    success: bool = asyncio.run(
        upload.main(namespace, *repos)
    )
    sys.exit(0 if success else 1)


@click.group()
def main() -> None:
    # main cli group
    pass


main.add_command(ammend_authors)
main.add_command(compute_bills)
main.add_command(upload_code)
