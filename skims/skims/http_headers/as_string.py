# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from more_itertools import (
    chunked,
)
from serializers import (
    make_snippet,
    SNIPPETS_COLUMNS,
    SnippetViewport,
)
from typing import (
    Dict,
    Optional,
)


def snippet(
    url: str,
    header: Optional[str],
    headers: Dict[str, str],
    columns_per_line: int = SNIPPETS_COLUMNS,
    value: str = "",
) -> str:
    line: int = 3
    found: bool = False
    content: str = f"> GET {url}\n> ...\n\n"

    for key, val in headers.items():
        line += 0 if found else 1
        if key == header and value in val:
            found = True

        if len(val) + len(key) + 6 > columns_per_line:
            content += f"< {key}:\n"
            for val_chunk in chunked(val, columns_per_line - 4):
                line += 0 if found else 1
                content += "    " + "".join(val_chunk) + "\n"
        else:
            content += f"< {key}: {val}\n"

    content += "\n* EOF"

    if not found:
        line += 2

    return make_snippet(
        content=content,
        viewport=SnippetViewport(
            columns_per_line=columns_per_line,
            column=0,
            line=line,
            wrap=True,
        ),
    )
