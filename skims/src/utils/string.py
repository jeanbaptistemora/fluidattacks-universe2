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
from typing import (
    List,
    Tuple,
)

# Third party libraries
from aioextensions import (
    unblock,
    unblock_cpu,
)
from PIL import (
    Image,
    ImageDraw,
    ImageFont,
)

# Local libraries
from utils.ctx import (
    get_artifact,
)
from utils.image import (
    blocking_clarify,
)


# Constants
DUMMY_IMG: Image = Image.new('RGB', (0, 0))
DUMMY_DRAWING: ImageDraw = ImageDraw.Draw(DUMMY_IMG)
FONT: ImageFont = ImageFont.truetype(
    font=get_artifact('vendor/fonts/roboto_mono_from_google/regular.ttf'),
    size=22,
)
WATERMARK: Image = blocking_clarify(
    image=Image.open(
        get_artifact('static/img/logo_fluid_attacks_854x329.png'),
    ),
    ratio=0.15,
)


def are_similar(string_a: str, string_b: str, threshold: float = 0.75) -> bool:
    return SequenceMatcher(None, string_a, string_b).ratio() >= threshold


async def to_in_memory_file(string: str) -> BytesIO:

    def _to_in_memory_file() -> BytesIO:
        return BytesIO(string.encode())

    return await unblock(_to_in_memory_file)


def blocking_to_snippet(
    *,
    chars_per_line: int = 120,
    column: int,
    content: str,
    context: int = 10,
    line: int,
) -> str:
    lines: Tuple[str, ...] = tuple(content.replace('\t', ' ').splitlines())
    number_of_lines: int = len(lines)
    zeros_needed: int = max(len(str(number_of_lines)), 2) + 2

    start_line: int = max(line - context - 1, 0)
    end_line: int = min(line + context, number_of_lines)

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
    chars_per_line: int = 120,
    column: int,
    content: str,
    context: int = 10,
    line: int,
) -> str:
    return await unblock_cpu(
        blocking_to_snippet,
        chars_per_line=chars_per_line,
        column=column,
        content=content,
        context=context,
        line=line,
    )


def blocking_boxify(
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
    string = blocking_boxify(string=string)

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
    return await unblock_cpu(_to_png, string=string)
