import pytest
import textwrap
from utils.string import (
    make_snippet,
    SnippetViewport,
)


def _dedent(content: str) -> str:
    return textwrap.dedent(content)[1:-1]


@pytest.mark.skims_test_group("unittesting")
def test_make_snippet() -> None:
    content = _dedent(
        """
        aaaaaaaaaabbbbbbbbbbcccccccccc
        ddddddddddeeeeeeeeeeffffffffff
        gggggggggghhhhhhhhhhiiiiiiiiii
        jjjjjjjjjjkkkkkkkkkkllllllllll
        """
    )
    assert make_snippet(content=content) == _dedent(
        """
        aaaaaaaaaabbbbbbbbbbcccccccccc
        ddddddddddeeeeeeeeeeffffffffff
        gggggggggghhhhhhhhhhiiiiiiiiii
        jjjjjjjjjjkkkkkkkkkkllllllllll
        """
    )

    assert make_snippet(
        content=content,
        viewport=SnippetViewport(
            columns_per_line=20,
            column=10,
            line=2,
            line_context=1,
            wrap=True,
        ),
    ) == _dedent(
        """
            | ccccc
        > 2 | dddddeeeeeeeeee
            | fffff
            ^ Col 5
        """
    )
