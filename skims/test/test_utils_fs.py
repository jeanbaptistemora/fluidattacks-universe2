# Third party libraries
from textwrap import (
    dedent,
)
from typing import (
    Tuple,
)

# Local libraries
from utils.aio import (
    block_decorator,
)
from utils.fs import (
    get_char_to_line_mapping,
)


@block_decorator
async def test_get_char_to_line_mapping() -> None:
    content: str = dedent("""
        x
        xx
        xxx
        xx
        x
    """)
    content_lines: Tuple[str, ...] = tuple(content.splitlines())

    assert await get_char_to_line_mapping(lines=content_lines) == {
        0: 1,
        1: 1,
        2: 2,
        3: 3,
        4: 4,
        5: 5,
        6: 5,
        7: 5,
        8: 5,
        9: 5,
        10: 5,
        11: 5,
        12: 5,
        13: 5,
        14: 5,
        len(content): 5,
    }
