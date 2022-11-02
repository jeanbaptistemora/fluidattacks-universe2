# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

import pytest
from serializers import (
    make_snippet,
    SnippetViewport,
)
import textwrap


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

    assert (
        make_snippet(
            content=_dedent(
                """
                1 center
                2
                3
                4
                5
                6
                """
            ),
            viewport=SnippetViewport(column=10, line=1, line_context=2),
        )
        == _dedent(
            """
            > 1 | 1 center
              2 | 2
              3 | 3
              4 | 4
              5 | 5
                ^ Col 0
            """
        )
    )
    assert (
        make_snippet(
            content=_dedent(
                """
                1
                2 center
                3
                4
                5
                6
                """
            ),
            viewport=SnippetViewport(column=10, line=2, line_context=2),
        )
        == _dedent(
            """
              1 | 1
            > 2 | 2 center
              3 | 3
              4 | 4
              5 | 5
                ^ Col 0
            """
        )
    )
    assert (
        make_snippet(
            content=_dedent(
                """
                1
                2
                3 center
                4
                5
                6
                """
            ),
            viewport=SnippetViewport(column=10, line=3, line_context=2),
        )
        == _dedent(
            """
              1 | 1
              2 | 2
            > 3 | 3 center
              4 | 4
              5 | 5
                ^ Col 0
            """
        )
    )
    assert (
        make_snippet(
            content=_dedent(
                """
                1
                2
                3
                4 center
                5
                6
                """
            ),
            viewport=SnippetViewport(column=10, line=4, line_context=2),
        )
        == _dedent(
            """
              2 | 2
              3 | 3
            > 4 | 4 center
              5 | 5
              6 | 6
                ^ Col 0
            """
        )
    )
    assert (
        make_snippet(
            content=_dedent(
                """
                1
                2
                3
                4
                5 center
                6
                """
            ),
            viewport=SnippetViewport(column=10, line=5, line_context=2),
        )
        == _dedent(
            """
              2 | 2
              3 | 3
              4 | 4
            > 5 | 5 center
              6 | 6
                ^ Col 0
            """
        )
    )
    assert (
        make_snippet(
            content=_dedent(
                """
                1
                2
                3
                4
                5
                6 center
                """
            ),
            viewport=SnippetViewport(column=10, line=6, line_context=2),
        )
        == _dedent(
            """
              2 | 2
              3 | 3
              4 | 4
              5 | 5
            > 6 | 6 center
                ^ Col 0
            """
        )
    )
