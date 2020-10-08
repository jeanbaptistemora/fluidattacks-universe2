# Standard library
import ast
from typing import (
    Awaitable,
    Callable,
    Iterator,
    List,
    Set,
    Tuple,
)

# Third party libraries
from aioextensions import (
    resolve,
    in_process,
)
from pyparsing import (
    delimitedList,
    Keyword,
    nestedExpr,
    Optional,
)

# Local libraries
from lib_path.common import (
    blocking_get_vulnerabilities,
    blocking_get_vulnerabilities_from_iterator,
    C_STYLE_COMMENT,
    DOUBLE_QUOTED_STRING,
    EXTENSIONS_CSHARP,
    EXTENSIONS_JAVA,
    EXTENSIONS_PYTHON,
    EXTENSIONS_SWIFT,
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


def _csharp_insecure_exceptions(
    content: str,
    path: str,
) -> Tuple[Vulnerability, ...]:
    insecure_exceptions: Set[str] = {
        # Generic
        'Exception',
        'ApplicationException',
        'SystemException',
        'System.Exception',
        'System.ApplicationException',
        'System.SystemException',

        # Unrecoverable
        'NullReferenceException',
        'system.NullReferenceException',
    }

    exception = VAR_ATTR_JAVA.copy()
    exception.addCondition(
        # Ensure that at least one exception in the group is the provided one
        lambda tokens: any(token in insecure_exceptions for token in tokens),
    )

    grammar = (
        Keyword('catch') +
        Optional(
            nestedExpr(
                closer=')',
                content=exception + Optional(VAR_ATTR_JAVA),
                ignoreExpr=None,
                opener='(',
            )
        ) +
        Optional(
            Keyword('when') +
            nestedExpr(opener='(', closer=')')
        ) +
        nestedExpr(opener='{', closer='}')
    )
    grammar.ignore(C_STYLE_COMMENT)
    grammar.ignore(DOUBLE_QUOTED_STRING)
    grammar.ignore(SINGLE_QUOTED_STRING)

    return blocking_get_vulnerabilities(
        content=content,
        cwe={'396'},
        description=t(
            key='src.lib_path.f060.insecure_exceptions.description',
            lang='C#',
            path=path,
        ),
        finding=FindingEnum.F060,
        grammar=grammar,
        path=path,
    )


@CACHE_ETERNALLY
@SHIELD
async def csharp_insecure_exceptions(
    content: str,
    path: str,
) -> Tuple[Vulnerability, ...]:
    return await in_process(
        _csharp_insecure_exceptions,
        content=content,
        path=path,
    )


def _java_insecure_exceptions(
    content: str,
    path: str,
) -> Tuple[Vulnerability, ...]:
    insecure_exceptions: Set[str] = {
        # Unrecoverable
        'RuntimeException',
        'lang.RuntimeException',
        'java.lang.RuntimeException',

        # Don't do this
        'NullPointerException',
        'lang.NullPointerException',
        'java.lang.NullPointerException',

        # Generics
        'Exception',
        'Throwable',
        'lang.Exception',
        'lang.Throwable',
        'java.lang.Exception',
        'java.lang.Throwable',
    }

    exception_group = delimitedList(expr=VAR_ATTR_JAVA, delim='|')
    exception_group.addCondition(
        # Ensure that at least one exception in the group is the provided one
        lambda tokens: any(token in insecure_exceptions for token in tokens),
    )

    grammar = (
        Keyword('catch') +
        nestedExpr(
            closer=')',
            content=exception_group + Optional(VAR_ATTR_JAVA),
            ignoreExpr=None,
            opener='(',
        )
    )
    grammar.ignore(C_STYLE_COMMENT)
    grammar.ignore(DOUBLE_QUOTED_STRING)
    grammar.ignore(SINGLE_QUOTED_STRING)

    return blocking_get_vulnerabilities(
        content=content,
        cwe={'396'},
        description=t(
            key='src.lib_path.f060.insecure_exceptions.description',
            lang='Java',
            path=path,
        ),
        finding=FindingEnum.F060,
        grammar=grammar,
        path=path,
    )


@CACHE_ETERNALLY
@SHIELD
async def java_insecure_exceptions(
    content: str,
    path: str,
) -> Tuple[Vulnerability, ...]:
    return await in_process(
        _java_insecure_exceptions,
        content=content,
        path=path,
    )


def _python_insecure_exceptions(
    content: str,
    path: str,
) -> Tuple[Vulnerability, ...]:
    node: ast.AST
    insecure: Set[str] = {'BaseException', 'Exception'}

    def are_names_insecure(*nodes: ast.AST) -> bool:
        return any(
            node.id in insecure for node in nodes if isinstance(node, ast.Name)
        )

    vulnerable_nodes: Iterator[ast.ExceptHandler] = iterate_nodes(
        content=content,
        filters=(
            lambda node: isinstance(node, ast.ExceptHandler),
            lambda node: any((
                node.type is None,
                (isinstance(node.type, ast.Name)
                    and are_names_insecure(node.type)),
                (isinstance(node.type, ast.Tuple)
                    and are_names_insecure(*node.type.elts)),
            )),
        ),
    )

    return blocking_get_vulnerabilities_from_iterator(
        content=content,
        cwe={'396'},
        description=t(
            key='src.lib_path.f060.insecure_exceptions.description',
            lang='Python',
            path=path,
        ),
        finding=FindingEnum.F060,
        iterator=(
            (node.lineno, node.col_offset) for node in vulnerable_nodes
        ),
        path=path,
    )


@CACHE_ETERNALLY
@SHIELD
async def python_insecure_exceptions(
    content: str,
    path: str,
) -> Tuple[Vulnerability, ...]:
    return await in_process(
        _python_insecure_exceptions,
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
        '{'
    )
    grammar.ignore(C_STYLE_COMMENT)
    grammar.ignore(DOUBLE_QUOTED_STRING)
    grammar.ignore(SINGLE_QUOTED_STRING)

    return blocking_get_vulnerabilities(
        content=content,
        cwe={'396'},
        description=t(
            key='src.lib_path.f060.insecure_exceptions.description',
            lang='Swift',
            path=path,
        ),
        finding=FindingEnum.F060,
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


async def analyze(
    content_generator: Callable[[], Awaitable[str]],
    file_extension: str,
    path: str,
    store: EphemeralStore,
) -> None:
    coroutines: List[Awaitable[Tuple[Vulnerability, ...]]] = []

    if file_extension in EXTENSIONS_CSHARP:
        coroutines.append(csharp_insecure_exceptions(
            content=await content_generator(),
            path=path,
        ))
    elif file_extension in EXTENSIONS_JAVA:
        coroutines.append(java_insecure_exceptions(
            content=await content_generator(),
            path=path,
        ))
    elif file_extension in EXTENSIONS_PYTHON:
        coroutines.append(python_insecure_exceptions(
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
