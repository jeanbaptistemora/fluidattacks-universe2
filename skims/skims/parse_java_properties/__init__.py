# Standard library
import contextlib
from typing import (
    Dict,
    Tuple,
)


def load(
    content: str,
    include_comments: bool = False,
) -> Dict[int, Tuple[str, str]]:
    mapping: Dict[int, Tuple[str, str]] = {}

    for line_no, line in enumerate(content.splitlines(), start=1):
        # Strip comments
        if not include_comments and '#' in line:
            line = line.split('#', maxsplit=1)[0]

        # Split in key and value
        with contextlib.suppress(ValueError):
            key, val = line.strip().split('=', maxsplit=1)
            key, val = key.strip(), val.strip()
            mapping[line_no] = (key, val)

    return mapping
