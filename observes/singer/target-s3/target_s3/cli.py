import click
from target_s3 import (
    loader,
)
from typing import (
    NoReturn,
)


@click.command()  # type: ignore[misc]
def main() -> NoReturn:
    loader.main().compute()
