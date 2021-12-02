import ast
from aws.model import (
    AWSCloudfrontDistribution,
    AWSCTrail,
    AWSDbInstance,
    AWSDynamoDBTable,
    AWSEbsEncryptionByDefault,
    AWSEbsVolume,
    AWSElb,
    AWSElbV2,
    AWSFSxFileSystem,
    AWSFsxWindowsFileSystem,
    AWSIamManagedPolicyArns,
    AWSIamPolicyStatement,
    AWSInstance,
    AWSKmsKey,
    AWSLaunchTemplate,
    AWSLbTargetGroup,
    AWSRdsCluster,
    AWSRdsClusterInstance,
    AWSS3Acl,
    AWSS3Bucket,
    AWSSecretsManagerSecret,
)
from frozendict import (  # type: ignore
    frozendict,
)
import inspect
import math
from metaloaders.model import (
    Node,
)
from model import (
    core_model,
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
from types import (
    FrameType,
)
from typing import (
    Any,
    Callable,
    cast,
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
    source_method = cast(
        FrameType, cast(FrameType, inspect.currentframe()).f_back
    ).f_code.co_name
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
                description=f"{t(key=description_key)} {t(key='words.in')} "
                f"{CTX.config.namespace}/{path}",
                snippet=make_snippet(
                    content=content,
                    viewport=SnippetViewport(
                        column=match.start_column,
                        line=match.start_line,
                        wrap=wrap,
                    ),
                ),
                source_method=source_method,
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
    source_method = cast(
        FrameType, cast(FrameType, inspect.currentframe()).f_back
    ).f_code.co_name
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
                description=f"{t(key=description_key)} {t(key='words.in')} "
                f"{CTX.config.namespace}/{path}",
                snippet=make_snippet(
                    content=content,
                    viewport=SnippetViewport(column=column_no, line=line_no),
                ),
                source_method=source_method,
            ),
        )
        for line_no, column_no in iterator
    )

    return results


def str_to_number(token: str, default: float = math.nan) -> float:
    try:
        return float(ast.literal_eval(token))
    except (SyntaxError, ValueError):
        return default


def get_line_by_extension(line: int, file_ext: str) -> int:
    return line - 1 if file_ext in EXTENSIONS_YAML else line


def get_aws_iterator(
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
            AWSFSxFileSystem,
            AWSFsxWindowsFileSystem,
            AWSEbsVolume,
            AWSInstance,
            AWSElb,
            AWSElbV2,
            AWSLaunchTemplate,
            AWSLbTargetGroup,
            AWSDbInstance,
            AWSRdsCluster,
            AWSRdsClusterInstance,
            AWSSecretsManagerSecret,
            Node,
        ]
    ],
) -> Iterator[Tuple[int, int]]:
    return (
        (
            stmt.start_line if isinstance(stmt, Node) else stmt.line,
            stmt.start_column if isinstance(stmt, Node) else stmt.column,
        )
        for stmt in statements_iterator
    )


def translate_dependencies_to_vulnerabilities(
    *,
    content: str,
    dependencies: Iterator[DependencyType],
    finding: core_model.FindingEnum,
    path: str,
    platform: core_model.Platform,
) -> core_model.Vulnerabilities:
    source_method = cast(
        FrameType, cast(FrameType, inspect.currentframe()).f_back
    ).f_code.co_name
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
                description=(
                    t(
                        key="src.lib_path.f011.npm_package_json.description",
                        product=product["item"],
                        version=version["item"],
                        cve=cve,
                    )
                    + f" {t(key='words.in')} {CTX.config.namespace}/{path}"
                ),
                snippet=make_snippet(
                    content=content,
                    viewport=SnippetViewport(
                        column=product["column"],
                        line=product["line"],
                    ),
                ),
                source_method=source_method,
            ),
        )
        for product, version in dependencies
        for cve in get_vulnerabilities(
            platform, product["item"], version["item"]
        )
    )

    return results
