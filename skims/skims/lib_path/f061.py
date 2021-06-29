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
    Empty,
    Keyword,
    nestedExpr,
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


def _python_swallows_exceptions(
    content: str,
    path: str,
) -> core_model.Vulnerabilities:
    node: ast.AST
    vulnerable_nodes: Iterator[ast.ExceptHandler] = iterate_nodes(
        content=content,
        filters=(
            lambda node: isinstance(node, ast.ExceptHandler),
            lambda node: hasattr(node, "body"),
            lambda node: bool(node.body),
            lambda node: all(isinstance(c, ast.Pass) for c in node.body),
        ),
    )

    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        cwe={"390"},
        description=t(
            key="src.lib_path.f061.swallows_exceptions.description",
            lang="Python",
            path=path,
        ),
        finding=core_model.FindingEnum.F061,
        iterator=((node.lineno, node.col_offset) for node in vulnerable_nodes),
        path=path,
    )


@CACHE_ETERNALLY
@SHIELD
@TIMEOUT_1MIN
async def python_swallows_exceptions(
    content: str,
    path: str,
) -> core_model.Vulnerabilities:
    return await in_process(
        _python_swallows_exceptions,
        content=content,
        path=path,
    )


def _swift_insecure_exceptions(
    content: str,
    path: str,
) -> core_model.Vulnerabilities:
    grammar = (
        Keyword("catch")
        + Optional("let" + VAR_ATTR_JAVA)
        + Optional("as" + VAR_ATTR_JAVA)
        + nestedExpr(opener="{", closer="}", content=~Empty())
    )
    grammar.ignore(C_STYLE_COMMENT)
    grammar.ignore(DOUBLE_QUOTED_STRING)
    grammar.ignore(SINGLE_QUOTED_STRING)

    return get_vulnerabilities_blocking(
        content=content,
        cwe={"390"},
        description=t(
            key="src.lib_path.f061.swallows_exceptions.description",
            lang="Swift",
            path=path,
        ),
        finding=core_model.FindingEnum.F061,
        grammar=grammar,
        path=path,
    )


@CACHE_ETERNALLY
@SHIELD
@TIMEOUT_1MIN
async def swift_insecure_exceptions(
    content: str,
    path: str,
) -> core_model.Vulnerabilities:
    return await in_process(
        _swift_insecure_exceptions,
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
            python_swallows_exceptions(
                content=await content_generator(),
                path=path,
            )
        )
    elif file_extension in EXTENSIONS_SWIFT:
        coroutines.append(
            swift_insecure_exceptions(
                content=await content_generator(),
                path=path,
            )
        )

    return coroutines
