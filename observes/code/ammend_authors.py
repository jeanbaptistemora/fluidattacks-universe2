"""Walks all data in Redshift and edit those authors accordingly to mailmap."""

# Standard library
import argparse
import re
from typing import (
    Dict,
    Match,
    Optional,
    Pattern,
    Tuple,
)

# Third party libraries
from aioextensions import (
    run,
)

# Local libraries
from shared import (
    log,
)

# Constants
WORKERS_COUNT: int = 8
MailmapMapping = Dict[Tuple[str, str], Tuple[str, str]]
"""Mapping from (author, email) to (canonical_author, canonical_email)."""


async def main(mailmap_dict: MailmapMapping) -> None:
    await log('info', '%s', mailmap_dict)


def get_mailmap_dict(mailmap_path: str) -> MailmapMapping:
    # This format is guaranteed by:
    #   https://github.com/kamadorueda/mailmap-linter
    #     /blob/5ae9d2654375afb76dfb3087b1e9b200257331a2/default.nix#L39
    mailmap_dict: MailmapMapping = {}
    mailmap_line: Pattern = re.compile(
        r'^(?P<canon_name>[A-Z][a-z]+ [A-Z][a-z]+) '
        r'<(?P<canon_email>.*)> '
        r'(?P<name>.*?) '
        r'<(?P<email>.*?)>$',
    )

    with open(mailmap_path) as file:
        for line in file.read().splitlines():
            match: Optional[Match] = mailmap_line.match(line)
            if match:
                mapping = match.groupdict()
                mailmap_from = (mapping['name'], mapping['email'])
                mailmap_to = (mapping['canon_name'], mapping['canon_email'])
                mailmap_dict[mailmap_from] = mailmap_to

    return mailmap_dict


def cli() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--mailmap-path', required=True)

    args = parser.parse_args()

    run(main(
        mailmap_dict=get_mailmap_dict(args.mailmap_path),
    ))


if __name__ == '__main__':
    cli()
