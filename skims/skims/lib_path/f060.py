from aioextensions import (
    in_process,
)
import ast
from lib_path.common import (
    C_STYLE_COMMENT,
    DOUBLE_QUOTED_STRING,
    EXTENSIONS_PYTHON,
    EXTENSIONS_SWIFT,
    get_vulnerabilities_blocking,
    get_vulnerabilities_from_iterator_blocking,
    SHIELD,
    SINGLE_QUOTED_STRING,
    VAR_ATTR_JAVA,
)
from model import (
    core_model,
)
from pyparsing import (
    Keyword,
    MatchFirst,
    Optional,
)
from state.cache import (
    CACHE_ETERNALLY,
)
from typing import (
    Awaitable,
    Callable,
    Iterator,
    List,
    Set,
)
from utils.ast import (
    iterate_nodes,
)
from utils.function import (
    TIMEOUT_1MIN,
)
from zone import (
    t,
)


def _python_insecure_exceptions(
    content: str,
    path: str,
) -> core_model.Vulnerabilities:
    node: ast.AST
    insecure: Set[str] = {"BaseException", "Exception"}

    def are_names_insecure(*nodes: ast.AST) -> bool:
        return any(
            node.id in insecure for node in nodes if isinstance(node, ast.Name)
        )

    vulnerable_nodes: Iterator[ast.ExceptHandler] = iterate_nodes(
        content=content,
        filters=(
            lambda node: isinstance(node, ast.ExceptHandler),
            lambda node: any(
                (
                    node.type is None,
                    (
                        isinstance(node.type, ast.Name)
                        and are_names_insecure(node.type)
                    ),
                    (
                        isinstance(node.type, ast.Tuple)
                        and are_names_insecure(*node.type.elts)
                    ),
                )
            ),
        ),
    )

    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        cwe={"396"},
        description=t(
            key="src.lib_path.f060.insecure_exceptions.description",
            lang="Python",
            path=path,
        ),
        finding=core_model.FindingEnum.F060,
        iterator=((node.lineno, node.col_offset) for node in vulnerable_nodes),
        path=path,
    )


@CACHE_ETERNALLY
@SHIELD
@TIMEOUT_1MIN
async def python_insecure_exceptions(
    content: str,
    path: str,
) -> core_model.Vulnerabilities:
    return await in_process(
        _python_insecure_exceptions,
        content=content,
        path=path,
    )


def _swift_generic_exceptions(
    content: str,
    path: str,
) -> core_model.Vulnerabilities:
    exc_generic = VAR_ATTR_JAVA.copy()
    exc_generic.addCondition(
        lambda tokens: tokens[0]
        in {
            "Error",
        }
    )

    grammar = (
        Keyword("catch")
        + MatchFirst(
            (
                Optional("let" + VAR_ATTR_JAVA + "as" + exc_generic),
                Optional("let" + VAR_ATTR_JAVA),
            )
        )
        + "{"
    )
    grammar.ignore(C_STYLE_COMMENT)
    grammar.ignore(DOUBLE_QUOTED_STRING)
    grammar.ignore(SINGLE_QUOTED_STRING)

    return get_vulnerabilities_blocking(
        content=content,
        cwe={"396"},
        description=t(
            key="src.lib_path.f060.insecure_exceptions.description",
            lang="Swift",
            path=path,
        ),
        finding=core_model.FindingEnum.F060,
        grammar=grammar,
        path=path,
    )


@CACHE_ETERNALLY
@SHIELD
@TIMEOUT_1MIN
async def swift_generic_exceptions(
    content: str,
    path: str,
) -> core_model.Vulnerabilities:
    return await in_process(
        _swift_generic_exceptions,
        content=content,
        path=path,
    )


@SHIELD
async def analyze(
    content_generator: Callable[[], Awaitable[str]],
    file_extension: str,
    path: str,
    **_: None,
) -> List[Awaitable[core_model.Vulnerabilities]]:
    coroutines: List[Awaitable[core_model.Vulnerabilities]] = []

    if file_extension in EXTENSIONS_PYTHON:
        coroutines.append(
            python_insecure_exceptions(
                content=await content_generator(),
                path=path,
            )
        )
    elif file_extension in EXTENSIONS_SWIFT:
        coroutines.append(
            swift_generic_exceptions(
                content=await content_generator(),
                path=path,
            )
        )

    return coroutines
