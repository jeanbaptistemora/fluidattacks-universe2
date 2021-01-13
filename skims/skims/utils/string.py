# Standard library
from difflib import (
    SequenceMatcher,
)
from io import (
    BytesIO,
)
from itertools import (
    chain,
    repeat,
)
import os
from typing import (
    List,
    Tuple,
)

# Third party libraries
from aioextensions import (
    in_process,
)
from PIL import (
    Image,
    ImageDraw,
    ImageFont,
)

# Local libraries
from utils.ctx import (
    FLUID_WATERMARK,
    ROBOTO_FONT,
    STATE_FOLDER_DEBUG,
)
from utils.image import (
    clarify_blocking,
)
from utils.logs import (
    log_blocking,
)

# Constants
DUMMY_IMG: Image = Image.new('RGB', (0, 0))
DUMMY_DRAWING: ImageDraw = ImageDraw.Draw(DUMMY_IMG)
FONT: ImageFont = ImageFont.truetype(
    font=ROBOTO_FONT,
    size=18,
)
WATERMARK: Image = clarify_blocking(
    image=Image.open(FLUID_WATERMARK),
    ratio=0.15,
)
SNIPPETS_CONTEXT: int = 10
SNIPPETS_COLUMNS: int = 12 * SNIPPETS_CONTEXT


def are_similar(string_a: str, string_b: str, threshold: float = 0.85) -> bool:
    return SequenceMatcher(None, string_a, string_b).ratio() >= threshold


def to_in_memory_file(string: str) -> BytesIO:
    return BytesIO(string.encode())


def to_snippet_blocking(
    *,
    chars_per_line: int = SNIPPETS_COLUMNS,
    column: int,
    content: str,
    context: int = SNIPPETS_CONTEXT,
    line: int,
) -> str:
    lines: Tuple[str, ...] = tuple(content.replace('\t', ' ').splitlines())
    number_of_lines: int = len(lines)
    zeros_needed: int = max(len(str(number_of_lines)), 2) + 2

    start_line: int = max(line - context // 2 - 1, 0)
    end_line: int = min(start_line + 2 * context + 1, number_of_lines)

    start_column: int = max(column - chars_per_line // 4, 0)
    end_column: int = start_column + chars_per_line

    separator: str = f'¦ {"-" * zeros_needed} ¦ {"-" * chars_per_line} ¦'
    snippet: str = '\n'.join(chain(
        [f'¦ {"line":^{zeros_needed}s} ¦ {"Data":<{chars_per_line}s} ¦'],
        [separator],
        (
            f'¦ {line_marker!s:>{zeros_needed}s} ¦ '
            f'{line_content[start_column:end_column]:<{chars_per_line}s} ¦'
            for line_no, line_content in enumerate(
                lines[start_line:end_line],
                start=start_line + 1,
            )
            for line_marker in [f'> {line_no}' if line_no == line else line_no]
        ),
        [separator],
        [f'  {"":^{zeros_needed}s} ^ Column {start_column}'],
    ))

    return snippet


async def to_snippet(
    *,
    chars_per_line: int = SNIPPETS_COLUMNS,
    column: int,
    content: str,
    context: int = SNIPPETS_CONTEXT,
    line: int,
) -> str:
    return await in_process(
        to_snippet_blocking,
        chars_per_line=chars_per_line,
        column=column,
        content=content,
        context=context,
        line=line,
    )


def boxify_blocking(
    *,
    width_to_height_ratio: int = 3,
    string: str,
) -> str:
    lines: List[str] = string.splitlines()

    width, height = max(map(len, lines)), len(lines)

    missing_height: int = width // width_to_height_ratio - height

    filling: List[str] = list(repeat('', missing_height // 2))

    return '\n'.join(filling + lines + filling)


def _to_png(*, string: str, margin: int = 25) -> BytesIO:
    # Make this image rectangular
    string = boxify_blocking(string=string)

    # This is the number of pixes needed to draw this text, may be big
    size: Tuple[int, int] = DUMMY_DRAWING.textsize(string, font=FONT)
    size = (
        size[0] + 2 * margin,
        size[1] + 2 * margin,
    )
    watermark_size: Tuple[int, int] = (
        size[0] // 2,
        WATERMARK.size[1] * size[0] // WATERMARK.size[0] // 2,
    )
    watermark_position: Tuple[int, int] = (
        (size[0] - watermark_size[0]) // 2,
        (size[1] - watermark_size[1]) // 2,
    )

    # Create an image with the right size to fit the snippet
    #  and resize it to a common resolution
    img: Image = Image.new('RGB', size, (0xff, 0xff, 0xff))

    drawing: ImageDraw = ImageDraw.Draw(img)
    drawing.multiline_text(
        xy=(margin, margin),
        text=string,
        fill=(0x33, 0x33, 0x33),
        font=FONT,
    )

    watermark = WATERMARK.resize(watermark_size)
    img.paste(watermark, watermark_position, watermark)

    stream: BytesIO = BytesIO()

    img.save(stream, format='PNG')

    stream.seek(0)

    return stream


async def to_png(*, string: str) -> BytesIO:
    return await in_process(_to_png, string=string)


def get_debug_path(path: str) -> str:
    output = os.path.join(
        STATE_FOLDER_DEBUG,
        os.path.relpath(path).replace('/', '__').replace('.', '_'),
    )
    log_blocking('info', 'An output will be generated at %s*', output)
    return output
