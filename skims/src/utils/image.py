# Standard library
from io import (
    BytesIO,
)
from typing import (
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


async def lines_to_png(
    *,
    chars_per_line: int = 160,
    content: str,
    context: int = 3,
    line: int,
    width_px: int = 1024,
) -> BytesIO:

    def _lines_to_png() -> BytesIO:
        lines: Tuple[str, ...] = tuple(content.splitlines())
        lines_number: int = len(lines)
        lines_10_power: int = len(str(lines_number))

        line_end: int = min(line + context, lines_number)
        line_start: int = max(line - context - 1, 0)

        snippet: str = '\n'.join(
            f'{str(line_no).zfill(lines_10_power)}'
            f' | '
            f'{line_content[0:chars_per_line].ljust(chars_per_line)}|'
            for line_no, line_content in enumerate(
                lines[line_start:line_end],
                start=line_start + 1,
            )
        )

        # Dummy images just to access their methods
        dummy_img: Image = Image.new('RGB', (0, 0))
        dummy_drawing: ImageDraw = ImageDraw.Draw(dummy_img)

        # This is the number of pixes needed to draw this text, may be big
        size: Tuple[int, int] = dummy_drawing.multiline_textsize(snippet)

        # Create an image with the right size to fit the snippet
        #  and resize it to a common resolution
        img: Image = Image.new('RGB', size)
        drawing: ImageDraw = ImageDraw.Draw(img)
        drawing.text((0, 0), snippet)
        img = img.resize((width_px, width_px * size[1] // size[0]))

        stream: BytesIO = BytesIO()

        img.save(stream, format='PNG')

        return stream

    return await unblock(_lines_to_png)
