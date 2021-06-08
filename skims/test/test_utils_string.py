import pytest
from textwrap import (
    dedent,
)
from utils.string import (
    make_snippet,
)


@pytest.mark.skims_test_group("unittesting")
def test_to_snippet() -> None:
    content: str = dedent(
        """
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
    """
    )

    snippet: str = make_snippet(
        chars_per_line=43,
        content=content,
        context=4,
        column=39,
        line=5,
    )

    assert (
        snippet
        == dedent(
            """
        ¦ line ¦ Data                                        ¦
        ¦ ---- ¦ ------------------------------------------- ¦
        ¦    3 ¦                                             ¦
        ¦    4 ¦                                             ¦
        ¦  > 5 ¦                                             ¦
        ¦    6 ¦                                             ¦
        ¦    7 ¦ x                                           ¦
        ¦    8 ¦ xxxxxxxxxxx                                 ¦
        ¦    9 ¦ x                                           ¦
        ¦   10 ¦                                             ¦
        ¦   11 ¦                                             ¦
        ¦ ---- ¦ ------------------------------------------- ¦
               ^ Column 29
    """
        )[1:-1]
    ), snippet
