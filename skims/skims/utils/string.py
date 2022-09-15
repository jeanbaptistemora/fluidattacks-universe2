# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from ctx import (
    STATE_FOLDER_DEBUG,
)
from io import (
    BytesIO,
)
from more_itertools import (
    chunked,
)
from operator import (
    itemgetter,
)
import os
from typing import (
    Iterator,
    List,
    NamedTuple,
    Optional,
    Set,
    Tuple,
)
from utils.logs import (
    log_blocking,
)

# Constants
SNIPPETS_CONTEXT: int = 10
SNIPPETS_COLUMNS: int = 12 * SNIPPETS_CONTEXT


def to_in_memory_file(string: str) -> BytesIO:
    return BytesIO(string.encode())


class SnippetViewport(NamedTuple):
    column: int
    line: int

    columns_per_line: int = SNIPPETS_COLUMNS
    line_context: int = SNIPPETS_CONTEXT
    wrap: bool = False


def _chunked(line: str, chunk_size: int) -> Iterator[str]:
    if line:
        yield from chunked(line, n=chunk_size)  # type: ignore
    else:
        yield ""


def make_snippet(
    *,
    content: str,
    viewport: Optional[SnippetViewport] = None,
) -> str:
    # Replace tab by spaces so 1 char renders as 1 symbol
    lines_raw: List[str] = content.replace("\t", " ").splitlines()

    # Build a list of line numbers to line contents, handling wrapping
    if viewport is not None and viewport.wrap:
        lines: List[Tuple[int, str]] = [
            (line_no, "".join(line_chunk))
            for line_no, line in enumerate(lines_raw, start=1)
            for line_chunk in _chunked(line, viewport.columns_per_line)
        ]
    else:
        lines = list(enumerate(lines_raw, start=1))

    if viewport is not None:
        # Find the vertical center of the snippet
        viewport_center = next(
            (
                index
                for index, (line_no, _) in enumerate(lines)
                if line_no == viewport.line
            ),
            0,
        )

        # Find the horizontal left of the snippet
        # We'll place the center at 25% from the left border
        viewport_left: int = max(
            viewport.column - viewport.columns_per_line // 4, 0
        )

        if lines:
            # How many chars do we need to write the line number
            loc_width: int = len(str(lines[-1][0]))

            # '>' highlights the line being marked
            line_no_last: Optional[int] = (
                lines[-2][0] if len(lines) >= 2 else None
            )
            for index, (line_no, line) in enumerate(lines):
                # Highlight this line if requested
                mark_symbol = (
                    ">"
                    if line_no == viewport.line and line_no != line_no_last
                    else " "
                )

                # Include the line number if not redundant
                line_no_str = "" if line_no == line_no_last else line_no
                line_no_last = line_no

                # Slice viewport horizontally
                line = line[
                    viewport_left : viewport_left
                    + viewport.columns_per_line
                    + 1
                ]

                # Edit in-place the lines to add the ruler
                fmt = f"{mark_symbol} {line_no_str!s:>{loc_width}s} | {line}"
                lines[index] = (line_no, fmt.rstrip(" "))

            # Slice viewport vertically
            if viewport_center - viewport.line_context <= 0:
                lines = lines[
                    slice(
                        0,
                        2 * viewport.line_context + 1,
                    )
                ]
            else:
                lines = lines[
                    slice(
                        max(viewport_center - viewport.line_context, 0),
                        viewport_center + viewport.line_context + 1,
                    )
                    if (viewport_center + viewport.line_context < len(lines))
                    else slice(
                        max(len(lines) - 2 * viewport.line_context - 1, 0),
                        len(lines),
                    )
                ]

            # Highlight the column if requested
            lines.append((0, f"  {' ':>{loc_width}} ^ Col {viewport_left}"))

    return "\n".join(map(itemgetter(1), lines))


def get_debug_path(path: str) -> str:
    output = os.path.join(
        STATE_FOLDER_DEBUG,
        os.path.relpath(path).replace("/", "__").replace(".", "_"),
    )
    log_blocking("info", "An output will be generated at %s*", output)
    return output


def build_attr_paths(*attrs: str) -> Set[str]:
    return set(".".join(attrs[index:]) for index, _ in enumerate(attrs))


def split_on_first_dot(string: str) -> Tuple[str, str]:
    portions = string.split(".", maxsplit=1)
    if len(portions) == 2:
        return portions[0], portions[1]
    return portions[0], ""


def split_on_last_dot(string: str) -> Tuple[str, str]:
    portions = string.rsplit(".", maxsplit=1)
    if len(portions) == 2:
        return portions[0], portions[1]
    return portions[0], ""


def complete_attrs_on_set(data: Set[str]) -> Set[str]:
    return {
        attr for path in data for attr in build_attr_paths(*path.split("."))
    }
