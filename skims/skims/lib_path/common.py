import ast
from aws.model import (
    AWSCloudfrontDistribution,
    AWSCTrail,
    AWSDbInstance,
    AWSDynamoDBTable,
    AWSEbsEncryptionByDefault,
    AWSEbsVolume,
    AWSElb,
    AWSFsxWindowsFileSystem,
    AWSIamManagedPolicyArns,
    AWSIamPolicyStatement,
    AWSInstance,
    AWSKmsKey,
    AWSLbTargetGroup,
    AWSRdsCluster,
    AWSS3Acl,
    AWSS3Bucket,
)
from frozendict import (  # type: ignore
    frozendict,
)
import math
from metaloaders.model import (
    Node,
)
from model import (
    core_model,
)
from model.graph_model import (
    NAttrs,
)
from pyparsing import (
    alphanums,
    alphas,
    col,
    cppStyleComment,
    delimitedList,
    lineno,
    ParserElement,
    pythonStyleComment,
    QuotedString,
    Word,
)
from sca import (
    get_vulnerabilities,
)
from typing import (
    Any,
    Callable,
    Iterable,
    Iterator,
    Set,
    Tuple,
    TypeVar,
    Union,
)
from utils.ctx import (
    CTX,
)
from utils.function import (
    shield,
)
from utils.string import (
    make_snippet,
    SnippetViewport,
)
from zone import (
    t,
)

# Constants
TFun = TypeVar("TFun", bound=Callable[..., Any])
DependencyType = Tuple[frozendict, frozendict]

# Reusable Components
C_STYLE_COMMENT: ParserElement = cppStyleComment
SHARP_STYLE_COMMENT: ParserElement = pythonStyleComment

NAMES_DOCKERFILE: Set[str] = {"Dockerfile"}
EXTENSIONS_CSHARP: Set[str] = {"cs"}
EXTENSIONS_JAVA: Set[str] = {"java"}
EXTENSIONS_JAVA_PROPERTIES: Set[str] = {"properties"}
EXTENSIONS_JAVASCRIPT: Set[str] = {"js", "jsx", "ts", "tsx"}
EXTENSIONS_JSON: Set[str] = {"json"}
EXTENSIONS_PYTHON: Set[str] = {"py", "pyw"}
EXTENSIONS_TERRAFORM: Set[str] = {"tf"}
EXTENSIONS_SWIFT: Set[str] = {"swift"}
EXTENSIONS_YAML: Set[str] = {"yml", "yaml"}
EXTENSIONS_CLOUDFORMATION: Set[str] = EXTENSIONS_YAML | EXTENSIONS_JSON
BACKTICK_QUOTED_STRING: QuotedString = QuotedString("`", escChar="\\")
SINGLE_QUOTED_STRING: QuotedString = QuotedString("'", escChar="\\")
DOUBLE_QUOTED_STRING: QuotedString = QuotedString('"', escChar="\\")
NUMBER: Word = Word("0123456789abcdefABCDEFxX.")
VAR_NAME_JAVA: ParserElement = Word(alphas + "$_", alphanums + "$_")
VAR_ATTR_JAVA: ParserElement = delimitedList(VAR_NAME_JAVA, ".", True)
TRUE_OPTIONS: Set[Union[str, bool, int]] = {"true", "True", True, "1", 1}
FALSE_OPTIONS: Set[Union[str, bool, int]] = {"false", "False", False, "0", 0}

SHIELD: Callable[[TFun], TFun] = shield(on_error_return=())

# Lint config
# pylint: disable=too-many-arguments


def get_matching_lines_blocking(
    content: str,
    grammar: ParserElement,
) -> Tuple[core_model.GrammarMatch, ...]:
    # Pyparsing's scanString expands tabs to 'n' number of spaces
    # But we count tabs as '1' char width
    # This forces the parser to not offset when a file contains tabs
    grammar.parseWithTabs()

    matches: Tuple[core_model.GrammarMatch, ...] = tuple(
        core_model.GrammarMatch(
            start_column=col(start_char, content) - 1,
            start_line=lineno(start_char, content),
        )
        for _, start_char, _ in grammar.scanString(content)
    )

    return matches


def get_vulnerabilities_blocking(
    content: str,
    cwe: Set[str],
    description_key: str,
    finding: core_model.FindingEnum,
    grammar: ParserElement,
    path: str,
    wrap: bool = False,
) -> core_model.Vulnerabilities:
    results: core_model.Vulnerabilities = tuple(
        core_model.Vulnerability(
            finding=finding,
            kind=core_model.VulnerabilityKindEnum.LINES,
            namespace=CTX.config.namespace,
            state=core_model.VulnerabilityStateEnum.OPEN,
            what=path,
            where=f"{match.start_line}",
            skims_metadata=core_model.SkimsVulnerabilityMetadata(
                cwe=tuple(cwe),
                description=t(
                    key=description_key,
                    path=f"{CTX.config.namespace}/{path}",
                ),
                snippet=make_snippet(
                    content=content,
                    viewport=SnippetViewport(
                        column=match.start_column,
                        line=match.start_line,
                        wrap=wrap,
                    ),
                ),
            ),
        )
        for match in get_matching_lines_blocking(
            content=content,
            grammar=grammar,
        )
    )

    return results


def get_vulnerabilities_from_iterator_blocking(
    content: str,
    cwe: Set[str],
    description_key: str,
    finding: core_model.FindingEnum,
    iterator: Iterator[Tuple[int, int]],
    path: str,
) -> core_model.Vulnerabilities:
    results: core_model.Vulnerabilities = tuple(
        core_model.Vulnerability(
            finding=finding,
            kind=core_model.VulnerabilityKindEnum.LINES,
            namespace=CTX.config.namespace,
            state=core_model.VulnerabilityStateEnum.OPEN,
            what=path,
            where=f"{line_no}",
            skims_metadata=core_model.SkimsVulnerabilityMetadata(
                cwe=tuple(cwe),
                description=t(
                    key=description_key,
                    path=f"{CTX.config.namespace}/{path}",
                ),
                snippet=make_snippet(
                    content=content,
                    viewport=SnippetViewport(column=column_no, line=line_no),
                ),
            ),
        )
        for line_no, column_no in iterator
    )

    return results


def get_vulnerabilities_from_n_attrs_iterable_blocking(
    content: str,
    cwe: Set[str],
    description: str,
    finding: core_model.FindingEnum,
    path: str,
    n_attrs_iterable: Iterable[NAttrs],
) -> core_model.Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        cwe=cwe,
        description_key=description,
        finding=finding,
        iterator=(
            (int(n_attrs["label_l"]), int(n_attrs["label_c"]))
            for n_attrs in n_attrs_iterable
        ),
        path=path,
    )


def str_to_number(token: str, default: float = math.nan) -> float:
    try:
        return float(ast.literal_eval(token))
    except (SyntaxError, ValueError):
        return default


def get_line_by_extension(line: int, file_ext: str) -> int:
    return line - 1 if file_ext in EXTENSIONS_YAML else line


def get_vulnerabilities_from_aws_iterator_blocking(
    content: str,
    description_key: str,
    finding: core_model.FindingEnum,
    path: str,
    statements_iterator: Iterator[
        Union[
            AWSCTrail,
            AWSDynamoDBTable,
            AWSEbsEncryptionByDefault,
            AWSIamManagedPolicyArns,
            AWSIamPolicyStatement,
            AWSKmsKey,
            AWSS3Acl,
            AWSS3Bucket,
            AWSCloudfrontDistribution,
            AWSFsxWindowsFileSystem,
            AWSEbsVolume,
            AWSInstance,
            AWSElb,
            AWSLbTargetGroup,
            AWSDbInstance,
            AWSRdsCluster,
            Node,
        ]
    ],
) -> core_model.Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        cwe={finding.value.cwe},
        description_key=description_key,
        finding=finding,
        iterator=(
            (
                stmt.start_line if isinstance(stmt, Node) else stmt.line,
                stmt.start_column if isinstance(stmt, Node) else stmt.column,
            )
            for stmt in statements_iterator
        ),
        path=path,
    )


def translate_dependencies_to_vulnerabilities(
    *,
    content: str,
    dependencies: Iterator[DependencyType],
    finding: core_model.FindingEnum,
    path: str,
    platform: core_model.Platform,
) -> core_model.Vulnerabilities:
    results: core_model.Vulnerabilities = tuple(
        core_model.Vulnerability(
            finding=finding,
            kind=core_model.VulnerabilityKindEnum.LINES,
            namespace=CTX.config.namespace,
            state=core_model.VulnerabilityStateEnum.OPEN,
            what=" ".join(
                (
                    path,
                    f'({product["item"]} v{version["item"]})',
                    f"[{cve}]",
                )
            ),
            where=f'{product["line"]}',
            skims_metadata=core_model.SkimsVulnerabilityMetadata(
                cwe=("937",),
                description=t(
                    key="src.lib_path.f011.npm_package_json.description",
                    path=f"{CTX.config.namespace}/{path}",
                    product=product["item"],
                    version=version["item"],
                    cve=cve,
                ),
                snippet=make_snippet(
                    content=content,
                    viewport=SnippetViewport(
                        column=product["column"],
                        line=product["line"],
                    ),
                ),
            ),
        )
        for product, version in dependencies
        for cve in get_vulnerabilities(
            platform, product["item"], version["item"]
        )
    )

    return results
