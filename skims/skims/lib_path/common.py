from aioextensions import (
    run,
)
import ast
from collections.abc import (
    Callable,
    Iterator,
)
from contextlib import (
    suppress,
)
from ctx import (
    CTX,
)
from dynamodb.resource import (
    dynamo_shutdown,
)
from frozendict import (
    frozendict,
)
from functools import (
    wraps,
)
from ipaddress import (
    AddressValueError,
    IPv4Network,
    IPv6Network,
)
import json_parser
from lark import (
    Tree,
)
import math
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
    makeHTMLTags,
    ParseException,
    ParserElement,
    pythonStyleComment,
    QuotedString,
    Word,
)
from sca import (
    get_vulnerabilities,
)
from serializers import (
    make_snippet,
    SnippetViewport,
)
from typing import (
    Any,
    TypeVar,
)
from utils.fs import (
    get_file_content_block,
)
from utils.function import (
    shield,
    shield_blocking,
)
from vulnerabilities import (
    build_lines_vuln,
    build_metadata,
)
from zone import (
    t,
)

# Constants
Tfun = TypeVar("Tfun", bound=Callable[..., Any])
DependencyType = tuple[frozendict, frozendict]

# Reusable Components
C_STYLE_COMMENT: ParserElement = cppStyleComment
SHARP_STYLE_COMMENT: ParserElement = pythonStyleComment

NAMES_DOCKERFILE: set[str] = {"Dockerfile"}
EXTENSIONS_BASH: set[str] = {"sh"}
EXTENSIONS_CSHARP: set[str] = {"cs"}
EXTENSIONS_JAVA: set[str] = {"java"}
EXTENSIONS_JAVA_PROPERTIES: set[str] = {"properties"}
EXTENSIONS_JAVASCRIPT: set[str] = {"js", "jsx", "ts", "tsx"}
EXTENSIONS_JSON: set[str] = {"json"}
EXTENSIONS_PYTHON: set[str] = {"py", "pyw"}
EXTENSIONS_TERRAFORM: set[str] = {"tf"}
EXTENSIONS_SWIFT: set[str] = {"swift"}
EXTENSIONS_YAML: set[str] = {"yml", "yaml"}
EXTENSIONS_CLOUDFORMATION: set[str] = EXTENSIONS_YAML | EXTENSIONS_JSON
BACKTICK_QUOTED_STRING: QuotedString = QuotedString("`", escChar="\\")
SINGLE_QUOTED_STRING: QuotedString = QuotedString("'", escChar="\\")
DOUBLE_QUOTED_STRING: QuotedString = QuotedString('"', escChar="\\")
NUMBER: Word = Word("0123456789abcdefABCDEFxX.")
VAR_NAME_JAVA: ParserElement = Word(alphas + "$_", alphanums + "$_")
VAR_ATTR_JAVA: ParserElement = delimitedList(VAR_NAME_JAVA, ".", True)
TRUE_OPTIONS: set[
    str | bool | int
] = {  # NOSONAR # pylint: disable=duplicate-value
    "true",
    "True",
    True,  # NOSONAR
    "1",
    1,
}
FALSE_OPTIONS: set[
    str | bool | int
] = {  # NOSONAR # pylint: disable=duplicate-value
    "false",
    "False",
    False,  # NOSONAR
    "0",
    0,
}

SHIELD: Callable[[Tfun], Tfun] = shield(on_error_return=())
SHIELD_BLOCKING: Callable[[Tfun], Tfun] = shield_blocking(on_error_return=())

# Lint config
# pylint: disable=too-many-arguments


def has_attributes(content: str, tag: str, attrs: dict) -> bool:
    """
    Check ``HTML`` attributes` values.

    This method checks whether the tag (``tag``) inside the code file
    has attributes (``attr``) with the specific values.

    :param tag: ``HTML`` tag to search.
    :param attrs: Attributes with values to search.
    :returns: True if attribute set as specified, False otherwise.
    """

    tag_s, _ = makeHTMLTags(tag)
    tag_expr = tag_s

    result = False

    for expr in tag_expr.searchString(content):
        for attr, value in attrs.items():
            try:
                value.parseString(getattr(expr, attr))
                result = True
            except ParseException:
                result = False
                break
        if result:
            break

    return result


def get_matching_lines_blocking(
    content: str,
    grammar: ParserElement,
) -> tuple[core_model.GrammarMatch, ...]:
    # Pyparsing's scanString expands tabs to 'n' number of spaces
    # But we count tabs as '1' char width
    # This forces the parser to not offset when a file contains tabs
    grammar.parseWithTabs()
    content = "\n".join(
        line for line in content.splitlines() if len(line) < 1000
    )
    matches: tuple[core_model.GrammarMatch, ...] = tuple(
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
                ).content,
            ),
        )
        for match in get_matching_lines_blocking(content, grammar)
    )

    return results


def get_vulnerabilities_from_iterator_blocking(
    content: str,
    description_key: str,
    iterator: Iterator[tuple[int, int]],
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
                ).content,
            ),
        )
        for line_no, column_no in iterator
    )

    return results


def get_vulnerabilities_include_parameter(
    content: str,
    description_key: str,
    iterator: Iterator[tuple[int, int, str]],
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
                description=(
                    t(
                        key=(description_key),
                        port=param,
                    )
                    + f" {t(key='words.in')} "
                    f"{CTX.config.namespace}/{path}"
                ),
                snippet=make_snippet(
                    content=content,
                    viewport=SnippetViewport(column=column_no, line=line_no),
                ).content,
            ),
        )
        for line_no, column_no, param in iterator
    )

    return results


def get_vulnerabilities_for_incomplete_deps(
    content: str,
    description_key: str,
    iterator: Iterator[str],
    path: str,
    method: core_model.MethodsEnum,
) -> core_model.Vulnerabilities:
    results: core_model.Vulnerabilities = tuple(
        build_lines_vuln(
            method=method,
            what=f"{path} (missing dependency: {dep})",
            where="0",
            metadata=build_metadata(
                method=method,
                description=f"{t(key=description_key)} {t(key='words.in')} "
                f"{CTX.config.namespace}/{path}",
                snippet=make_snippet(
                    content=content,
                    viewport=SnippetViewport(column=int(0), line=int(0)),
                ).content,
            ),
        )
        for dep in iterator
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
) -> Iterator[tuple[int, int]]:
    return (
        (
            stmt.start_line if hasattr(stmt, "start_line") else stmt.line,
            stmt.start_column
            if hasattr(stmt, "start_column")
            else stmt.column,
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
    return run(
        _translate_dependencies_to_vulnerabilities(
            content=content,
            dependencies=dependencies,
            path=path,
            platform=platform,
            method=method,
        )
    )


async def _translate_dependencies_to_vulnerabilities(
    *,
    content: str,
    dependencies: Iterator[DependencyType],
    path: str,
    platform: core_model.Platform,
    method: core_model.MethodsEnum,
) -> core_model.Vulnerabilities:
    try:
        # pylint: disable=consider-using-generator
        results: core_model.Vulnerabilities = tuple(
            [
                build_lines_vuln(
                    method=method,
                    what=" ".join(
                        (
                            path,
                            f'({product["item"]} v{version["item"]})',
                            f"[{', '.join(cve)}]",
                        )
                    ),
                    where=str(product["line"]),
                    metadata=build_metadata(
                        method=method,
                        description=(
                            t(
                                key=(
                                    "src.lib_path.f011."
                                    "npm_package_json.description"
                                ),
                                product=product["item"],
                                version=version["item"],
                                cve=cve,
                            )
                            + f" {t(key='words.in')} "
                            f"{CTX.config.namespace}/{path}"
                        ),
                        snippet=make_snippet(
                            content=content,
                            viewport=SnippetViewport(
                                column=product["column"],
                                line=product["line"],
                            ),
                        ).content,
                    ),
                )
                for product, version in dependencies
                if (
                    cve := await get_vulnerabilities(
                        platform, product["item"], version["item"]
                    )
                )
            ]
        )
    finally:
        await dynamo_shutdown()

    return results


def get_subdependencies(package: str, yarn_dict: lockfile) -> tuple:
    subdependencies: list[str] = []
    version: str | None = None
    for pkg_key, pkg_info in yarn_dict.items():
        # There may be keys in the yarn.lock file like this:
        # pkg@v1, pkg@v2, pkg@v3
        pkg_list = pkg_key.split(", ")
        if package in pkg_list:
            version = pkg_info.get("version")
            if "dependencies" in pkg_info:
                subdependencies = build_subdep_name(pkg_info["dependencies"])
    return subdependencies, version


def add_lines_enumeration(
    windower: Iterator[
        tuple[tuple[int, str], tuple[int, str]],
    ],
    tree: dict[str, str],
) -> dict[str, dict[str, Any]]:
    enumerated_tree: dict[str, dict[str, Any]] = {}
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
                enumerated_tree[product] = {
                    "version": version,
                    "product_line": product_line,
                    "version_line": version_line,
                }
    return enumerated_tree


def build_subdep_name(dependencies: dict[str, str]) -> list[str]:
    dependencies_list: list[str] = []
    for key, value in dependencies.items():
        dependencies_list.append(key + "@" + value)
    return dependencies_list


def run_over_subdeps(
    subdeps: list[str], tree: dict[str, str], yarn_dict: lockfile
) -> dict[str, str]:
    while subdeps:
        current_subdep = subdeps[0]
        new_subdeps, version = get_subdependencies(current_subdep, yarn_dict)
        if version:
            tree[current_subdep] = version
        subdeps.remove(current_subdep)
        subdeps = [
            subdep
            for subdep in subdeps + new_subdeps
            if subdep not in tree  # Avoid infite loop with cyclic dependencies
        ]
    return tree


def build_dependencies_tree(  # pylint: disable=too-many-locals
    path_yarn: str,
    path_json: str,
    dependencies_type: core_model.DependenciesTypeEnum,
) -> dict[str, dict[str, Any]]:
    # Dependencies type could be "devDependencies" for dev dependencies
    # or "dependencies" for prod dependencies
    enumerated_tree: dict[str, dict[str, Any]] = {}
    yarn_content = get_file_content_block(path_yarn)
    windower: Iterator[
        tuple[tuple[int, str], tuple[int, str]]
    ] = windowed(  # type: ignore
        fillvalue="",
        n=2,
        seq=tuple(enumerate(yarn_content.splitlines(), start=1)),
        step=1,
    )
    yarn_dict = lockfile.Lockfile.from_file(path_yarn).data
    package_json_parser = json_parser.parse(get_file_content_block(path_json))
    tree: dict[str, str] = {}
    if dependencies_type.value in package_json_parser:
        package_json_dict = package_json_parser[dependencies_type.value]
        for json_pkg_name, json_pkg_version in package_json_dict.items():
            for yarn_pkg_key, yarn_pkg_info in yarn_dict.items():
                # There may be keys in the yarn.lock file like this:
                # pkg@v1, pkg@v2, pkg@v3
                yarn_pkg_list = yarn_pkg_key.split(", ")
                json_pkg = json_pkg_name + "@" + json_pkg_version
                if json_pkg in yarn_pkg_list:
                    tree[json_pkg] = yarn_pkg_info["version"]
                    if "dependencies" in yarn_pkg_info:
                        subdeps = build_subdep_name(
                            yarn_pkg_info["dependencies"]
                        )
                        tree = run_over_subdeps(subdeps, tree, yarn_dict)
        enumerated_tree = add_lines_enumeration(windower, tree)
    return enumerated_tree


def format_pkg_dep(
    pkg_name: Any,
    version: Any,
    product_line: Any,
    version_line: Any,
    column: Any = 0,
) -> DependencyType:

    return (
        {
            "column": column,
            "line": product_line,
            "item": pkg_name,
        },
        {
            "column": column,
            "line": version_line,
            "item": version,
        },
    )


def pkg_deps_to_vulns(
    platform: core_model.Platform, method: core_model.MethodsEnum
) -> Callable[[Tfun], Callable[[str, str], core_model.Vulnerabilities]]:
    def resolve_deps(
        resolve_dependencies: Tfun,
    ) -> Callable[[str, str], core_model.Vulnerabilities]:
        @wraps(resolve_dependencies)
        def resolve_vulns(
            content: str, path: str
        ) -> core_model.Vulnerabilities:

            return translate_dependencies_to_vulnerabilities(
                content=content,
                dependencies=resolve_dependencies(content, path),
                path=path,
                platform=platform,
                method=method,
            )

        return resolve_vulns

    return resolve_deps


def validate_port_values(from_port: Any, to_port: Any) -> bool:
    if (
        not isinstance(from_port.val, dict)
        and not isinstance(from_port.val, Tree)
        and not isinstance(to_port.val, dict)
        and not isinstance(to_port.val, Tree)
    ):
        return True
    return False
