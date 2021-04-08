# Standard library
from typing import (
    Any,
    Dict,
)

# Local libraries
from utils.string import (
    to_snippet_blocking,
)


def snippet(
    url: str,
    header: str,
    headers: Dict[str, str],
    **kwargs: Any,
) -> str:
    line: int = 3
    found: bool = False
    content: str = f'> GET {url}\n> ...\n\n'

    for key, val in headers.items():
        line += 0 if found else 1
        content += f'< {key}: {val}\n'
        if key == header:
            found = True

    content += '\n* EOF'

    if not found:
        line += 2

    return to_snippet_blocking(
        content=content,
        column=0,
        line=line,
        **kwargs,
    )
