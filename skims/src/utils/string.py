# Standard library
from difflib import SequenceMatcher
from io import (
    BytesIO,
)
from itertools import (
    accumulate,
)
from itertools import (
    chain,
)
from typing import (
    Dict,
    Tuple,
)

# Third party libraries
from PIL import (
    Image,
    ImageDraw,
)

# Local libraries
from utils.aio import (
    unblock,
)


async def get_char_to_yx_map(
    *,
    lines: Tuple[str, ...],
) -> Dict[int, Tuple[int, int]]:

    def _get_char_to_yx_map() -> Dict[int, Tuple[int, int]]:
        mapping: Dict[int, Tuple[int, int]] = {}

        if not lines:
            return mapping

        # Add 1 to take into account for the new line
        cumulated_lines_length: Tuple[int, ...] = tuple(
            accumulate(len(line) + 1 for line in lines),
        )

        line: int = 0
        column: int = 0
        for char_number in range(1, cumulated_lines_length[-1] + 1):
            mapping[char_number - 1] = (line + 1, column)

            if char_number == cumulated_lines_length[line]:
                line += 1
                column = 0
            else:
                column += 1

        return mapping

    return await unblock(_get_char_to_yx_map)


def are_similar(string_a: str, string_b: str, threshold: float = 0.85) -> bool:
    return SequenceMatcher(None, string_a, string_b).ratio() >= threshold


async def to_in_memory_file(string: str) -> BytesIO:

    def _to_in_memory_file() -> BytesIO:
        return BytesIO(string.encode())

    return await unblock(_to_in_memory_file)


async def to_snippet(
    *,
    chars_per_line: int = 160,
    column: int,
    content: str,
    context: int = 10,
    line: int,
) -> str:

    def _to_snippet() -> str:
        lines: Tuple[str, ...] = tuple(content.splitlines())
        number_of_lines: int = len(lines)
        zeros_needed: int = max(len(str(number_of_lines)), 4)

        start_line: int = max(line - context - 1, 0)
        end_line: int = min(line + context, number_of_lines)

        start_column: int = max(column - chars_per_line // 2, 0)
        end_column: int = start_column + chars_per_line

        separator: str = f'¦ {"-" * zeros_needed} ¦ {"-" * chars_per_line} ¦'
        snippet: str = '\n'.join(chain(
            [f'¦ {"line":^{zeros_needed}s} ¦ {"File":<{chars_per_line}s} ¦'],
            [separator],
            (
                f'¦ {line_no!s:>{zeros_needed}s} ¦ '
                f'{line_content[start_column:end_column]:<{chars_per_line}s} ¦'
                for line_no, line_content in enumerate(
                    lines[start_line:end_line],
                    start=start_line + 1,
                )
            ),
            [separator],
            [f'  {"":^{zeros_needed}s} ^ Column {start_column}'],
        ))

        return snippet

    return await unblock(_to_snippet)


async def to_png(
    *,
    chars_per_line: int = 160,
    column: int,
    content: str,
    context: int = 10,
    line: int,
    width_px: int = 1024,
) -> BytesIO:

    snippet: str = await to_snippet(
        chars_per_line=chars_per_line,
        content=content,
        context=context,
        column=column,
        line=line,
    )

    def _string_to_png() -> BytesIO:
        # Dummy images just to access their methods
        dummy_img: Image = Image.new('RGB', (0, 0))
        dummy_drawing: ImageDraw = ImageDraw.Draw(dummy_img)

        # This is the number of pixes needed to draw this text, may be big
        size: Tuple[int, int] = dummy_drawing.multiline_textsize(snippet)

        # Create an image with the right size to fit the snippet
        #  and resize it to a common resolution
        img: Image = Image.new('RGB', size, (0x27, 0x28, 0x22))
        drawing: ImageDraw = ImageDraw.Draw(img)
        drawing.multiline_text((0, 0), snippet, (0xEE, 0xEE, 0xEC))
        img = img.resize((width_px, width_px * size[1] // size[0]))

        stream: BytesIO = BytesIO()

        img.save('test.png', format='PNG')

        return stream

    return await unblock(_string_to_png)
