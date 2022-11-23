import click
import sys
from tap_csv import (
    receiver,
)
from typing import (
    IO,
)


@click.command()
@click.option(
    "--tap-input", help="tap inputs", type=click.File("r"), default=sys.stdin
)
def main(tap_input: IO[str]) -> None:
    receiver.process_stdin(tap_input)
