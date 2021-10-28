import asyncio
import click
from code_etl import (
    compute_bills as bills,
    upload,
)
from os.path import (
    abspath,
)
from returns.maybe import (
    Maybe,
)
import sys
from typing import (
    Iterator,
    Optional,
    Tuple,
)


@click.command()
@click.argument("folder", type=str)
@click.argument("year", type=int)
@click.argument("month", type=int)
@click.argument("integrates_token", type=str)
def compute_bills(
    folder: str, year: int, month: int, integrates_token: str
) -> None:
    bills.main(
        folder,
        year,
        month,
        integrates_token,
    )


mailmap_file = click.Path(
    exists=True,
    file_okay=True,
    dir_okay=False,
    writable=False,
    readable=True,
    resolve_path=True,
    allow_dash=False,
    path_type=str,
)


@click.command()
@click.argument("namespace", type=str)
@click.argument("repositories", type=str, nargs=-1)
@click.option("--mailmap", type=mailmap_file)
def upload_code(
    namespace: str, repositories: Tuple[str, ...], mailmap: Optional[str]
) -> None:
    repos: Iterator[str] = map(abspath, repositories)
    success: bool = asyncio.run(
        upload.main(Maybe.from_optional(mailmap), namespace, *repos)
    )
    sys.exit(0 if success else 1)


@click.group()
def main() -> None:
    # main cli group
    pass


main.add_command(compute_bills)
main.add_command(upload_code)
