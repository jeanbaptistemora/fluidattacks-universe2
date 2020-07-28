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
from utils.string import (
    to_snippet,
)


@block_decorator
async def test_to_snippet() -> None:
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

    snippet: str = await to_snippet(
        chars_per_line=43,
        content=content,
        context=4,
        column=50,
        line=5,
    )

    assert snippet == dedent("""
        ¦ line ¦ File                                        ¦
        ¦ ---- ¦ ------------------------------------------- ¦
        ¦    1 ¦                                             ¦
        ¦    2 ¦                                             ¦
        ¦    3 ¦                                             ¦
        ¦    4 ¦                                             ¦
        ¦    5 ¦                                             ¦
        ¦    6 ¦                                             ¦
        ¦    7 ¦ x                                           ¦
        ¦    8 ¦ xxxxxxxxxxx                                 ¦
        ¦    9 ¦ x                                           ¦
        ¦ ---- ¦ ------------------------------------------- ¦
               ^ Column 29
    """)[1:-1], snippet
