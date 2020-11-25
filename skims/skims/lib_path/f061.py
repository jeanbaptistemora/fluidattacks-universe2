# Standard library
import ast
from typing import (
    Awaitable,
    Callable,
    Iterator,
    List,
    Tuple,
)

# Third party libraries
from aioextensions import (
    resolve,
    in_process,
)
from pyparsing import (
    Empty,
    Keyword,
    MatchFirst,
    nestedExpr,
    Optional,
)

# Local libraries
from lib_path.common import (
    blocking_get_vulnerabilities,
    blocking_get_vulnerabilities_from_iterator,
    C_STYLE_COMMENT,
    EXTENSIONS_CSHARP,
    EXTENSIONS_JAVA,
    EXTENSIONS_JAVASCRIPT,
    EXTENSIONS_PYTHON,
    EXTENSIONS_SWIFT,
    DOUBLE_QUOTED_STRING,
    SHIELD,
    SINGLE_QUOTED_STRING,
    VAR_ATTR_JAVA,
)
from state.cache import (
    CACHE_ETERNALLY,
)
from state.ephemeral import (
    EphemeralStore,
)
from utils.ast import (
    iterate_nodes,
)
from utils.model import (
    FindingEnum,
    Vulnerability,
)
from zone import (
    t,
)


def _csharp_swallows_exceptions(
    content: str,
    path: str,
) -> Tuple[Vulnerability, ...]:
    # Empty() grammar matches 'anything'
    # ~Empty() grammar matches 'not anything' or 'nothing'
    grammar = (
        Keyword('catch') +
        Optional(nestedExpr(opener='(', closer=')')) +
        Optional(Keyword('when') + nestedExpr(opener='(', closer=')')) +
        nestedExpr(opener='{', closer='}', content=~Empty())
    )
    grammar.ignore(C_STYLE_COMMENT)
    grammar.ignore(DOUBLE_QUOTED_STRING)
    grammar.ignore(SINGLE_QUOTED_STRING)

    return blocking_get_vulnerabilities(
        content=content,
        cwe={'390'},
        description=t(
            key='src.lib_path.f061.swallows_exceptions.description',
            lang='C#',
            path=path,
        ),
        finding=FindingEnum.F061,
        grammar=grammar,
        path=path,
    )


@CACHE_ETERNALLY
@SHIELD
async def csharp_swallows_exceptions(
    content: str,
    path: str,
) -> Tuple[Vulnerability, ...]:
    return await in_process(
        _csharp_swallows_exceptions,
        content=content,
        path=path,
    )


def _javascript_swallows_exceptions(
    content: str,
    path: str,
) -> Tuple[Vulnerability, ...]:
    # Empty() grammar matches 'anything'
    # ~Empty() grammar matches 'not anything' or 'nothing'
    classic = (
        Keyword('catch') +
        Optional(nestedExpr(opener='(', closer=')')) +
        nestedExpr(opener='{', closer='}', content=~Empty())
    )
    modern = (
        '.' +
        Keyword('catch') +
        nestedExpr(opener='(', closer=')', content=~Empty())
    )

    grammar = MatchFirst([classic, modern])
    grammar.ignore(C_STYLE_COMMENT)
    grammar.ignore(DOUBLE_QUOTED_STRING)
    grammar.ignore(SINGLE_QUOTED_STRING)

    return blocking_get_vulnerabilities(
        content=content,
        cwe={'390'},
        description=t(
            key='src.lib_path.f061.swallows_exceptions.description',
            lang='Javascript',
            path=path,
        ),
        finding=FindingEnum.F061,
        grammar=grammar,
        path=path,
    )


@CACHE_ETERNALLY
@SHIELD
async def javascript_swallows_exceptions(
    content: str,
    path: str,
) -> Tuple[Vulnerability, ...]:
    return await in_process(
        _javascript_swallows_exceptions,
        content=content,
        path=path,
    )


def _java_swallows_exceptions(
    content: str,
    path: str,
) -> Tuple[Vulnerability, ...]:
    # Empty() grammar matches 'anything'
    # ~Empty() grammar matches 'not anything' or 'nothing'
    grammar = (
        Keyword('catch') +
        nestedExpr(opener='(', closer=')') +
        nestedExpr(opener='{', closer='}', content=~Empty())
    )
    grammar.ignore(C_STYLE_COMMENT)
    grammar.ignore(DOUBLE_QUOTED_STRING)
    grammar.ignore(SINGLE_QUOTED_STRING)

    return blocking_get_vulnerabilities(
        content=content,
        cwe={'390'},
        description=t(
            key='src.lib_path.f061.swallows_exceptions.description',
            lang='Java',
            path=path,
        ),
        finding=FindingEnum.F061,
        grammar=grammar,
        path=path,
    )


@CACHE_ETERNALLY
@SHIELD
async def java_swallows_exceptions(
    content: str,
    path: str,
) -> Tuple[Vulnerability, ...]:
    return await in_process(
        _java_swallows_exceptions,
        content=content,
        path=path,
    )


def _python_swallows_exceptions(
    content: str,
    path: str,
) -> Tuple[Vulnerability, ...]:
    node: ast.AST
    vulnerable_nodes: Iterator[ast.ExceptHandler] = iterate_nodes(
        content=content,
        filters=(
            lambda node: isinstance(node, ast.ExceptHandler),
            lambda node: hasattr(node, 'body'),
            lambda node: bool(node.body),
            lambda node: all(isinstance(c, ast.Pass) for c in node.body),
        ),
    )

    return blocking_get_vulnerabilities_from_iterator(
        content=content,
        cwe={'390'},
        description=t(
            key='src.lib_path.f061.swallows_exceptions.description',
            lang='Python',
            path=path,
        ),
        finding=FindingEnum.F061,
        iterator=(
            (node.lineno, node.col_offset) for node in vulnerable_nodes
        ),
        path=path,
    )


@CACHE_ETERNALLY
@SHIELD
async def python_swallows_exceptions(
    content: str,
    path: str,
) -> Tuple[Vulnerability, ...]:
    return await in_process(
        _python_swallows_exceptions,
        content=content,
        path=path,
    )


def _swift_insecure_exceptions(
    content: str,
    path: str,
) -> Tuple[Vulnerability, ...]:
    grammar = (
        Keyword('catch') +
        Optional('let' + VAR_ATTR_JAVA) +
        Optional('as' + VAR_ATTR_JAVA) +
        nestedExpr(opener='{', closer='}', content=~Empty())
    )
    grammar.ignore(C_STYLE_COMMENT)
    grammar.ignore(DOUBLE_QUOTED_STRING)
    grammar.ignore(SINGLE_QUOTED_STRING)

    return blocking_get_vulnerabilities(
        content=content,
        cwe={'390'},
        description=t(
            key='src.lib_path.f061.swallows_exceptions.description',
            lang='Swift',
            path=path,
        ),
        finding=FindingEnum.F061,
        grammar=grammar,
        path=path,
    )


@CACHE_ETERNALLY
@SHIELD
async def swift_insecure_exceptions(
    content: str,
    path: str,
) -> Tuple[Vulnerability, ...]:
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
    store: EphemeralStore,
) -> None:
    coroutines: List[Awaitable[Tuple[Vulnerability, ...]]] = []

    if file_extension in EXTENSIONS_CSHARP:
        coroutines.append(csharp_swallows_exceptions(
            content=await content_generator(),
            path=path,
        ))
    elif file_extension in EXTENSIONS_JAVA:
        coroutines.append(java_swallows_exceptions(
            content=await content_generator(),
            path=path,
        ))
    elif file_extension in EXTENSIONS_JAVASCRIPT:
        coroutines.append(javascript_swallows_exceptions(
            content=await content_generator(),
            path=path,
        ))
    elif file_extension in EXTENSIONS_PYTHON:
        coroutines.append(python_swallows_exceptions(
            content=await content_generator(),
            path=path,
        ))
    elif file_extension in EXTENSIONS_SWIFT:
        coroutines.append(swift_insecure_exceptions(
            content=await content_generator(),
            path=path,
        ))

    for results in resolve(coroutines, worker_greediness=1):
        for result in await results:
            await store.store(result)
