# Standard library
from itertools import (
    accumulate
)
from typing import (
    Dict,
    NamedTuple,
    Tuple,
)

# Third party libraries
from pyparsing import (
    cppStyleComment,
    ParserElement,
    QuotedString,
)

# Local libraries
from utils.model import (
    GrammarMatch,
)

# Reusable Components
C_STYLE_COMMENT: ParserElement = cppStyleComment

SINGLE_QUOTED_STRING: QuotedString = QuotedString("'")
DOUBLE_QUOTED_STRING: QuotedString = QuotedString('"')


def blocking_get_matching_lines(
    content: str,
    char_to_yx_map: Dict[int, int],
    grammar: ParserElement,
) -> Tuple[GrammarMatch, ...]:
    # Pyparsing's scanString expands tabs to 'n' number of spaces
    # But we count tabs as '1' char width
    # This forces the parser to not offset when a file contains tabs
    grammar.parseWithTabs()

    matches: Tuple[GrammarMatch, ...] = tuple(
        GrammarMatch(
            start_char=start_char,
            start_column=start_column,
            start_line=start_line,
            end_char=end_char,
            end_column=end_column,
            end_line=end_line,
        )

        for _, start_char, end_char in grammar.scanString(content)
        for start_line, start_column in [char_to_yx_map[start_char]]
        for end_line, end_column in [char_to_yx_map[end_char]]
    )

    return matches
