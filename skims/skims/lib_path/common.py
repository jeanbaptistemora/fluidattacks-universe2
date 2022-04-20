import ast
from contextlib import (
    suppress,
)
from ctx import (
    CTX,
)
from frozendict import (  # type: ignore
    frozendict,
)
from ipaddress import (
    AddressValueError,
    IPv4Network,
    IPv6Network,
)
import json_parser
import math
from metaloaders.model import (
    Node,
)
from model import (
    core_model,
)
from more_itertools import (
    windowed,
)
from pyarn import (
    lockfile,
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
    Dict,
    Iterator,
    List,
    Set,
    Tuple,
    TypeVar,
    Union,
)
from utils.fs import (
    get_file_content_block,
)
from utils.function import (
    shield,
    shield_blocking,
)
from utils.string import (
    make_snippet,
    SnippetViewport,
)
from vulnerabilities import (
    build_lines_vuln,
    build_metadata,
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
SHIELD_BLOCKING: Callable[[TFun], TFun] = shield_blocking(on_error_return=())

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
    description_key: str,
    grammar: ParserElement,
    path: str,
    method: core_model.MethodsEnum,
    wrap: bool = False,
) -> core_model.Vulnerabilities:
    results: core_model.Vulnerabilities = tuple(
        build_lines_vuln(
            method=method,
            what=path,
            where=str(match.start_line),
            metadata=build_metadata(
                method=method,
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
            ),
        )
        for match in get_matching_lines_blocking(content, grammar)
    )

    return results


def get_vulnerabilities_from_iterator_blocking(
    content: str,
    description_key: str,
    iterator: Iterator[Tuple[int, int]],
    path: str,
    method: core_model.MethodsEnum,
) -> core_model.Vulnerabilities:
    results: core_model.Vulnerabilities = tuple(
        build_lines_vuln(
            method=method,
            what=path,
            where=str(line_no),
            metadata=build_metadata(
                method=method,
                description=f"{t(key=description_key)} {t(key='words.in')} "
                f"{CTX.config.namespace}/{path}",
                snippet=make_snippet(
                    content=content,
                    viewport=SnippetViewport(column=column_no, line=line_no),
                ),
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


def is_cidr(cidr: str) -> bool:
    """Validate if a string is a valid CIDR."""
    result = False
    with suppress(AddressValueError, ValueError):
        IPv4Network(cidr, strict=False)
        result = True
    with suppress(AddressValueError, ValueError):
        IPv6Network(cidr, strict=False)
        result = True
    return result


def get_cloud_iterator(
    statements_iterator: Iterator[Any],
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
    path: str,
    platform: core_model.Platform,
    method: core_model.MethodsEnum,
) -> core_model.Vulnerabilities:
    results: core_model.Vulnerabilities = tuple(
        build_lines_vuln(
            method=method,
            what=" ".join(
                (
                    path,
                    f'({product["item"]} v{version["item"]})',
                    f"[{cve}]",
                )
            ),
            where=str(product["line"]),
            metadata=build_metadata(
                method=method,
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
            ),
        )
        for product, version in dependencies
        for cve in get_vulnerabilities(
            platform, product["item"], version["item"]
        )
    )

    return results


def get_subdependencies(current_subdep: str, data: Any) -> Tuple:
    for yarn in data:
        if yarn.find(current_subdep) != -1:
            yarn_dict: Any = data.get(yarn)
            if "dependencies" in yarn_dict.keys():
                return (
                    build_subdep_name(yarn_dict.get("dependencies")),
                    yarn_dict.get("version"),
                    yarn,
                )
            return [], yarn_dict.get("version"), yarn
    return [], None, None


def add_lines(
    windower: Iterator[
        Tuple[Tuple[int, str], Tuple[int, str]],
    ],
    tree: Dict[str, Any],
) -> Dict[str, Any]:

    for (product_line, product), (version_line, version) in windower:
        product, version = product.strip(), version.strip()
        if (
            product.endswith(":")
            and not product.startswith(" ")
            and version.startswith("version")
        ):
            product = product.rstrip(":")
            product = product.strip('"')

            version = version.split(" ", maxsplit=1)[1]
            version = version.strip('"')

            if tree.get(product) == version:
                tree[product] = {
                    "version": version,
                    "product_line": product_line,
                    "version_line": version_line,
                }
    return tree


def build_subdep_name(dependencies: Dict[str, Any]) -> List[str]:
    dependencies_list: List[str] = []
    for key, value in dependencies.items():
        dependencies_list.append(key + "@" + value)
    return dependencies_list


def build_dependencies_tree(  # pylint: disable=too-many-locals,
    # pylint: disable=too-many-nested-blocks
    path_yarn: str,
    path_json: str,
    dependencies_type: str,
) -> Dict[str, Any]:
    # Dependencies type could be "devDependencies" for dev dependencies
    # or "dependencies" for prod dependencies
    yarn_content = get_file_content_block(path_yarn)
    windower: Iterator[Tuple[Tuple[int, str], Tuple[int, str]]] = windowed(
        fillvalue="",
        n=2,
        seq=tuple(enumerate(yarn_content.splitlines(), start=1)),
        step=1,
    )
    yarn_dict = lockfile.Lockfile.from_file(path_yarn).data
    package_parser = json_parser.parse(get_file_content_block(path_json))
    tree: Dict[str, Any] = {}
    if dependencies_type in package_parser:
        package_dict = package_parser[dependencies_type]
        for json_key, json_value in package_dict.items():
            for yarn_key, yarn_value in yarn_dict.items():
                dep = json_key + "@" + json_value
                if dep.find(yarn_key) != -1:
                    tree[dep] = yarn_value["version"]
                    if "dependencies" in yarn_value:
                        subdeps = build_subdep_name(yarn_value["dependencies"])
                        while subdeps:
                            current_subdep = subdeps[0]
                            new_values, version, name = get_subdependencies(
                                current_subdep, yarn_dict
                            )
                            tree[name] = version
                            subdeps.remove(current_subdep)
                            subdeps = subdeps + new_values
        tree = add_lines(windower, tree)
    return tree
