from more_itertools import (
    chunked,
)
from operator import (
    itemgetter,
)
from typing import (
    Iterator,
    List,
    NamedTuple,
    Optional,
    Tuple,
)

# Constants
SNIPPETS_CONTEXT: int = 10
SNIPPETS_COLUMNS: int = 12 * SNIPPETS_CONTEXT


class SnippetViewport(NamedTuple):
    line: int
    column: Optional[int] = None

    columns_per_line: int = SNIPPETS_COLUMNS
    line_context: int = SNIPPETS_CONTEXT
    wrap: bool = False
    show_line_numbers: bool = True
    highlight_line_number: bool = True


class Snippet(NamedTuple):
    content: str
    offset: int
    line: Optional[int] = None
    column: Optional[int] = None
    columns_per_line: int = SNIPPETS_COLUMNS
    line_context: int = SNIPPETS_CONTEXT
    wrap: bool = False
    show_line_numbers: bool = True
    highlight_line_number: bool = True


def _chunked(line: str, chunk_size: int) -> Iterator[str]:
    if line:
        yield from chunked(line, n=chunk_size)  # type: ignore
    else:
        yield ""


def make_snippet(  # NOSONAR
    *,
    content: str,
    viewport: Optional[SnippetViewport] = None,
) -> Snippet:
    # Replace tab by spaces so 1 char renders as 1 symbol
    lines_raw: List[str] = content.replace("\t", " ").splitlines()
    offset = 0
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
        viewport_left: int = (
            max(viewport.column - viewport.columns_per_line // 4, 0)
            if viewport.column is not None
            else 0
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
                    if line_no == viewport.line
                    and line_no != line_no_last
                    and viewport.highlight_line_number
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
                if viewport.show_line_numbers:
                    fmt = (
                        f"{mark_symbol} {line_no_str!s:>{loc_width}s} | {line}"
                    )
                    lines[index] = (line_no, fmt.rstrip(" "))
                else:
                    lines[index] = (line_no, line)

            # Slice viewport vertically
            if viewport_center - viewport.line_context <= 0:
                offset = 0
                lines = lines[
                    slice(
                        0,
                        2 * viewport.line_context + 1,
                    )
                ]
            else:
                offset = (
                    max(viewport_center - viewport.line_context, 0)
                    if (viewport_center + viewport.line_context < len(lines))
                    else max(len(lines) - 2 * viewport.line_context - 1, 0)
                )
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

            if (
                viewport.column is not None
                and viewport.show_line_numbers
                and viewport.highlight_line_number
            ):
                lines.append(
                    (0, f"  {' ':>{loc_width}} ^ Col {viewport_left}")
                )

    if viewport:
        return Snippet(
            content="\n".join(map(itemgetter(1), lines)),
            offset=offset,
            line=viewport.line,
            column=viewport.column,
            columns_per_line=viewport.columns_per_line,
            line_context=viewport.line_context,
            highlight_line_number=viewport.highlight_line_number,
            show_line_numbers=viewport.show_line_numbers,
            wrap=viewport.wrap,
        )

    return Snippet(
        content="\n".join(map(itemgetter(1), lines)),
        offset=offset,
    )
