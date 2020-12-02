# Standard libraries
from typing import IO
# Third party libraries
import click
# Local libraries
from tap_csv import core
from tap_csv.core import AdjustCsvOptions


@click.command()
@click.argument('csv_file', type=click.File('r'))
@click.argument('stream', type=str)
@click.option(
    '--quote-nonnum', default=False, help='transform csv with QUOTE_NONNUMERIC'
)
@click.option('--no-pkeys', default=False, help='no primary keys in file')
@click.option('--no-types', default=False, help='no field types in file')
def main(
    csv_file: IO[str],
    stream: str,
    quote_nonnum: bool,
    no_pkeys: bool,
    no_types: bool
) -> None:
    options = AdjustCsvOptions(
        quote_nonnum=quote_nonnum,
        add_default_types=no_types,
        pkeys_present=not no_pkeys,
    )
    core.to_singer(csv_file, stream, options)
