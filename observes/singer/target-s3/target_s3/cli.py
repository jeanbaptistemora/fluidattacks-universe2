from . import (
    loader,
)
import click
from typing import (
    NoReturn,
)


@click.command()  # type: ignore[misc]
def main() -> NoReturn:
    loader.main().compute()
