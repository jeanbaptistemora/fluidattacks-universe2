# Standard library
from typing import (
    Any,
    Callable,
    Dict,
    Set,
    Tuple,
    TypeVar,
)

# Third party libraries
from pyparsing import (
    alphas,
    alphanums,
    cppStyleComment,
    delimitedList,
    ParserElement,
    pythonStyleComment,
    QuotedString,
    Word,
)

# Local libraries
from utils.function import (
    retry,
)
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

# Constants
TFun = TypeVar('TFun', bound=Callable[..., Any])

# Reusable Components
C_STYLE_COMMENT: ParserElement = cppStyleComment
SHARP_STYLE_COMMENT: ParserElement = pythonStyleComment

NAMES_DOCKERFILE: Set[str] = {'Dockerfile'}
EXTENSIONS_CSHARP: Set[str] = {'cs'}
EXTENSIONS_JAVA: Set[str] = {'class', 'java'}
EXTENSIONS_JAVASCRIPT: Set[str] = {'js', 'jsx', 'ts', 'tsx'}
EXTENSIONS_JSON: Set[str] = {'json'}
EXTENSIONS_PYTHON: Set[str] = {'py', 'pyw'}
EXTENSIONS_SWIFT: Set[str] = {'swift'}
EXTENSIONS_YAML: Set[str] = {'yml', 'yaml'}
BACKTICK_QUOTED_STRING: QuotedString = QuotedString("`", escChar='\\')
SINGLE_QUOTED_STRING: QuotedString = QuotedString("'", escChar='\\')
DOUBLE_QUOTED_STRING: QuotedString = QuotedString('"', escChar='\\')

VAR_NAME_JAVA: ParserElement = Word(alphas + '$_', alphanums + '$_')
VAR_ATTR_JAVA: ParserElement = delimitedList(VAR_NAME_JAVA, '.', True)

HANDLE_ERRORS: Callable[[TFun], TFun] = retry(
    attempts=1,
    on_error=(),
    on_exceptions=(
        RecursionError,
    ),
)


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
            start_column=start_column,
            start_line=start_line,
        )
        for _, start_char, _ in grammar.scanString(content)
        for start_line, start_column in [char_to_yx_map[start_char]]
    )

    return matches


def blocking_get_vulnerabilities(  # pylint: disable=too-many-arguments
    char_to_yx_map: Dict[int, Tuple[int, int]],
    content: str,
    description: str,
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
                description=description,
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
