# Third party libraries
from textwrap import (
    dedent,
)
from typing import (
    Tuple,
)

# Third party libraries
from aioextensions import (
    block_decorator,
)

# Local libraries
from utils.string import (
    get_char_to_yx_map,
    blocking_to_snippet,
)


def test_to_snippet() -> None:
    content: str = dedent("""
        xxxxx
        xxxxxxxxxx
        xxxxxxxxxxxxxxx
        xxxxxxxxxxxxxxxxxxxx
        xxxxxxxxxxxxxxxxxxxxxxxxx
        xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
        xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
        xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
        xxxxxxxxxxxxxxxxxxxxxxxxx
        xxxxxxxxxxxxxxxxxxxx
        xxxxxxxxxxxxxxx
        xxxxxxxxxx
        xxxxx
    """)

    snippet: str = blocking_to_snippet(
        chars_per_line=43,
        content=content,
        context=4,
        column=39,
        line=5,
    )

    assert snippet == dedent("""
        ¦ line ¦ Data                                        ¦
        ¦ ---- ¦ ------------------------------------------- ¦
        ¦    1 ¦                                             ¦
        ¦    2 ¦                                             ¦
        ¦    3 ¦                                             ¦
        ¦    4 ¦                                             ¦
        ¦  > 5 ¦                                             ¦
        ¦    6 ¦                                             ¦
        ¦    7 ¦ x                                           ¦
        ¦    8 ¦ xxxxxxxxxxx                                 ¦
        ¦    9 ¦ x                                           ¦
        ¦ ---- ¦ ------------------------------------------- ¦
               ^ Column 29
    """)[1:-1], snippet


@block_decorator
async def test_get_char_to_yx_map() -> None:
    content: str = dedent("""
        x
        xx
        xxx
        xx
        x
    """)[1:-1]
    content_lines: Tuple[str, ...] = tuple(content.splitlines())

    assert await get_char_to_yx_map(lines=content_lines) == {
        0: (1, 0),
        1: (1, 1),
        2: (2, 0),
        3: (2, 1),
        4: (2, 2),
        5: (3, 0),
        6: (3, 1),
        7: (3, 2),
        8: (3, 3),
        9: (4, 0),
        10: (4, 1),
        11: (4, 2),
        12: (5, 0),
        13: (5, 1),
    }
