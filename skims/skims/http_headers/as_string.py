# Standard library
from typing import (
    Any,
    Dict,
    Optional,
)

# Third party libraries
from more_itertools import (
    chunked,
)

# Local libraries
from utils.string import (
    SNIPPETS_COLUMNS,
    to_snippet_blocking,
)


def snippet(
    url: str,
    header: Optional[str],
    headers: Dict[str, str],
    **kwargs: Any,
) -> str:
    chars_per_line: int = kwargs.get('chars_per_line') or SNIPPETS_COLUMNS
    line: int = 3
    found: bool = False
    content: str = f'> GET {url}\n> ...\n\n'

    for key, val in headers.items():
        line += 0 if found else 1
        if key == header:
            found = True

        if len(val) + len(key) + 6 > chars_per_line:
            content += f'< {key}:\n'
            for val_chunk in chunked(val, chars_per_line - 4):
                line += 0 if found else 1
                content += '    ' + "".join(val_chunk) + '\n'
        else:
            content += f'< {key}: {val}\n'

    content += '\n* EOF'

    if not found:
        line += 2

    return to_snippet_blocking(
        content=content,
        column=0,
        line=line,
        **kwargs,
    )
