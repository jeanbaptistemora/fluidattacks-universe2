# Standard library
from itertools import (
    accumulate
)
from typing import (
    Dict,
    Tuple,
)

# Third party libraries
from pyparsing import (
    cppStyleComment,
    ParserElement,
    QuotedString,
)

# Reusable Components
C_STYLE_COMMENT: ParserElement = cppStyleComment

SINGLE_QUOTED_STRING: QuotedString = QuotedString("'")
DOUBLE_QUOTED_STRING: QuotedString = QuotedString('"')


def blocking_get_matching_lines(
    content: str,
    char_to_line_mapping: Dict[int, int],
    grammar: ParserElement,
) -> Tuple[int, ...]:
    # Pyparsing's scanString expands tabs to 'n' number of spaces
    # But we count tabs as '1' char width
    # This forces the parser to not offset when a file contains tabs
    grammar.parseWithTabs()

    vulnerabilities: Tuple[int, ...] = tuple(
        char_to_line_mapping[start]
        for _, start, _ in grammar.scanString(content)
    )

    return vulnerabilities
