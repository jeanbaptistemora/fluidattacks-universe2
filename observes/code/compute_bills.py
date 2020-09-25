"""Process Redshift data and compute bills for every namespace."""

# Standard library
import argparse

# Third party libraries
from aioextensions import (
    run,
)

# Local libraries
from shared import (
    log,
)


async def main(year: int, month: int) -> None:
    await log('info', 'Computing bills for year: %s, month: %s', year, month)


def cli() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--year', type=int, required=True)
    parser.add_argument('--month', type=int, required=True)
    args = parser.parse_args()

    run(main(args.year, args.month))


if __name__ == '__main__':
    cli()
