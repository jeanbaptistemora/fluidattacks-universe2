"""Walks all data in Redshift and edit those authors accordingly to mailmap."""

# Standard library
import re
from typing import (
    Dict,
    Match,
    Optional,
    Pattern,
    Tuple,
)

# Third party libraries

# Local libraries

# Constants
MailmapMapping = Dict[Tuple[str, str], Tuple[str, str]]


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
                if mailmap_from != mailmap_to:
                    mailmap_dict[mailmap_from] = mailmap_to

    return mailmap_dict
