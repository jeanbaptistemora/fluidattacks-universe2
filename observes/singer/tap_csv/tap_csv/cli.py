# Standard libraries
import sys
from typing import IO
# Third party libraries
import click
# Local libraries
from tap_csv import receiver


@click.command()
@click.option(
    '--tap-input',
    help='tap inputs',
    type=click.File('r'),
    default=sys.stdin
)
def main(tap_input: IO[str]) -> None:
    receiver.process_stdin(tap_input)
