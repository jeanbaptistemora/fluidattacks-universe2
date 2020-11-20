# Standard library
import ast
import math
from typing import (
    Any,
    Callable,
    Iterator,
    Set,
    Tuple,
    TypeVar,
    Union,
)

# Third party libraries
from metaloaders.model import (
    Node,
)
from pyparsing import (
    alphas,
    alphanums,
    col,
    cppStyleComment,
    delimitedList,
    lineno,
    ParserElement,
    pythonStyleComment,
    QuotedString,
    Word,
)

# Local libraries
from aws.model import (
    AWSIamManagedPolicyArns,
    AWSIamPolicyStatement,
    AWSS3Acl,
    AWSS3Bucket,
)
from utils.function import (
    shield,
)
from utils.graph import (
    NAttrs,
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
from zone import (
    t,
)

# Constants
TFun = TypeVar('TFun', bound=Callable[..., Any])

# Reusable Components
C_STYLE_COMMENT: ParserElement = cppStyleComment
SHARP_STYLE_COMMENT: ParserElement = pythonStyleComment

NAMES_DOCKERFILE: Set[str] = {'Dockerfile'}
EXTENSIONS_CSHARP: Set[str] = {'cs'}
EXTENSIONS_JAVA: Set[str] = {'java'}
EXTENSIONS_JAVA_PROPERTIES: Set[str] = {'properties'}
EXTENSIONS_JAVASCRIPT: Set[str] = {'js', 'jsx', 'ts', 'tsx'}
EXTENSIONS_JSON: Set[str] = {'json'}
EXTENSIONS_PYTHON: Set[str] = {'py', 'pyw'}
EXTENSIONS_TERRAFORM: Set[str] = {'tf'}
EXTENSIONS_SWIFT: Set[str] = {'swift'}
EXTENSIONS_YAML: Set[str] = {'yml', 'yaml'}
EXTENSIONS_CLOUDFORMATION: Set[str] = EXTENSIONS_YAML | EXTENSIONS_JSON
BACKTICK_QUOTED_STRING: QuotedString = QuotedString("`", escChar='\\')
SINGLE_QUOTED_STRING: QuotedString = QuotedString("'", escChar='\\')
DOUBLE_QUOTED_STRING: QuotedString = QuotedString('"', escChar='\\')
NUMBER: Word = Word('0123456789abcdefABCDEFxX.')
VAR_NAME_JAVA: ParserElement = Word(alphas + '$_', alphanums + '$_')
VAR_ATTR_JAVA: ParserElement = delimitedList(VAR_NAME_JAVA, '.', True)

SHIELD: Callable[[TFun], TFun] = shield(on_error_return=())

# Lint config
# pylint: disable=too-many-arguments


def blocking_get_matching_lines(
    content: str,
    grammar: ParserElement,
) -> Tuple[GrammarMatch, ...]:
    # Pyparsing's scanString expands tabs to 'n' number of spaces
    # But we count tabs as '1' char width
    # This forces the parser to not offset when a file contains tabs
    grammar.parseWithTabs()

    matches: Tuple[GrammarMatch, ...] = tuple(
        GrammarMatch(
            start_column=col(start_char, content) - 1,
            start_line=lineno(start_char, content),
        )
        for _, start_char, _ in grammar.scanString(content)
    )

    return matches


def blocking_get_vulnerabilities(
    content: str,
    cwe: Set[str],
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
                cwe=tuple(cwe),
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
            grammar=grammar,
        )
    )

    return results


def blocking_get_vulnerabilities_from_iterator(
    content: str,
    cwe: Set[str],
    description: str,
    finding: FindingEnum,
    iterator: Iterator[Tuple[int, int]],
    path: str,
) -> Tuple[Vulnerability, ...]:
    results: Tuple[Vulnerability, ...] = tuple(
        Vulnerability(
            finding=finding,
            kind=VulnerabilityKindEnum.LINES,
            state=VulnerabilityStateEnum.OPEN,
            what=path,
            where=f'{line_no}',
            skims_metadata=SkimsVulnerabilityMetadata(
                cwe=tuple(cwe),
                description=description,
                snippet=blocking_to_snippet(
                    column=column_no,
                    content=content,
                    line=line_no,
                )
            )
        )
        for line_no, column_no in iterator
    )

    return results


def blocking_get_vulnerabilities_from_n_attrs_iterator(
    content: str,
    cwe: Set[str],
    description: str,
    finding: FindingEnum,
    n_attrs_iterator: Iterator[NAttrs],
    path: str,
) -> Tuple[Vulnerability, ...]:
    return blocking_get_vulnerabilities_from_iterator(
        content=content,
        cwe=cwe,
        description=description,
        finding=finding,
        iterator=(
            (int(n_attrs['label_l']), int(n_attrs['label_c']))
            for n_attrs in n_attrs_iterator
        ),
        path=path,
    )


def str_to_number(token: str, default: float = math.nan) -> float:
    try:
        return float(ast.literal_eval(token))
    except (SyntaxError, ValueError):
        return default


def blocking_get_vulnerabilities_from_aws_iterator(
    content: str,
    description_key: str,
    finding: FindingEnum,
    path: str,
    statements_iterator: Iterator[Union[
        AWSIamManagedPolicyArns,
        AWSIamPolicyStatement,
        AWSS3Acl,
        AWSS3Bucket,
        Node,
    ]],
) -> Tuple[Vulnerability, ...]:
    return blocking_get_vulnerabilities_from_iterator(
        content=content,
        cwe={finding.value.cwe},
        description=t(
            key=description_key,
            path=path,
        ),
        finding=finding,
        iterator=((
            stmt.start_line if isinstance(stmt, Node) else stmt.line,
            stmt.start_column if isinstance(stmt, Node) else stmt.column,
        ) for stmt in statements_iterator),
        path=path,
    )
