# Standard library
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

# Local libraries
from utils.model import (
    FindingEnum,
    GrammarMatch,
    SkimsVulnerabilityMetadata,
    Vulnerability,
    VulnerabilityKindEnum,
    VulnerabilityStateEnum,
)
from utils.string import (
    blocking_to_snippet,
)

# Reusable Components
C_STYLE_COMMENT: ParserElement = cppStyleComment

EXTENSIONS_CSHARP = ('cs',)
EXTENSIONS_JAVA = ('class', 'java')
EXTENSIONS_JAVASCRIPT = ('js', 'jsx', 'ts', 'tsx')

SINGLE_QUOTED_STRING: QuotedString = QuotedString("'")
DOUBLE_QUOTED_STRING: QuotedString = QuotedString('"')


def blocking_get_matching_lines(
    content: str,
    char_to_yx_map: Dict[int, Tuple[int, int]],
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


def blocking_get_vulnerabilities(
    char_to_yx_map: Dict[int, Tuple[int, int]],
    content: str,
    finding: FindingEnum,
    grammar: ParserElement,
    path: str,
) -> Tuple[Vulnerability, ...]:
    results: Tuple[Vulnerability, ...] = tuple(
        Vulnerability(
            finding=finding,
            kind=VulnerabilityKindEnum.LINES,
            state=VulnerabilityStateEnum.OPEN,
            what=path,
            where=f'{match.start_line}',
            skims_metadata=SkimsVulnerabilityMetadata(
                grammar_match=match,
                snippet=blocking_to_snippet(
                    column=match.start_column,
                    content=content,
                    line=match.start_line,
                )
            )
        )
        for match in blocking_get_matching_lines(
            content=content,
            char_to_yx_map=char_to_yx_map,
            grammar=grammar,
        )
    )

    return results
