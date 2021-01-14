# Standard library
import ast
from typing import (
    Awaitable,
    Callable,
    Iterator,
    List,
    Set,
)

# Third party libraries
from aioextensions import (
    in_process,
)
from pyparsing import (
    delimitedList,
    Keyword,
    MatchFirst,
    nestedExpr,
    Optional,
)

# Local libraries
from lib_path.common import (
    get_vulnerabilities_blocking,
    get_vulnerabilities_from_iterator_blocking,
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
from utils.function import (
    TIMEOUT_1MIN,
)
from utils.ast import (
    iterate_nodes,
)
from model.core_model import (
    FindingEnum,
    Vulnerabilities,
)
from zone import (
    t,
)


def _csharp_insecure_exceptions(
    content: str,
    path: str,
) -> Vulnerabilities:
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

    return get_vulnerabilities_blocking(
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
@TIMEOUT_1MIN
async def csharp_insecure_exceptions(
    content: str,
    path: str,
) -> Vulnerabilities:
    return await in_process(
        _csharp_insecure_exceptions,
        content=content,
        path=path,
    )


def _java_insecure_exceptions(
    content: str,
    path: str,
) -> Vulnerabilities:
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

    return get_vulnerabilities_blocking(
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
@TIMEOUT_1MIN
async def java_insecure_exceptions(
    content: str,
    path: str,
) -> Vulnerabilities:
    return await in_process(
        _java_insecure_exceptions,
        content=content,
        path=path,
    )


def _python_insecure_exceptions(
    content: str,
    path: str,
) -> Vulnerabilities:
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

    return get_vulnerabilities_from_iterator_blocking(
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
@TIMEOUT_1MIN
async def python_insecure_exceptions(
    content: str,
    path: str,
) -> Vulnerabilities:
    return await in_process(
        _python_insecure_exceptions,
        content=content,
        path=path,
    )


def _swift_generic_exceptions(
    content: str,
    path: str,
) -> Vulnerabilities:
    exc_generic = VAR_ATTR_JAVA.copy()
    exc_generic.addCondition(lambda tokens: tokens[0] in {
        'Error',
    })

    grammar = (
        Keyword('catch') +
        MatchFirst((
            Optional('let' + VAR_ATTR_JAVA + 'as' + exc_generic),
            Optional('let' + VAR_ATTR_JAVA),
        )) +
        '{'
    )
    grammar.ignore(C_STYLE_COMMENT)
    grammar.ignore(DOUBLE_QUOTED_STRING)
    grammar.ignore(SINGLE_QUOTED_STRING)

    return get_vulnerabilities_blocking(
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
@TIMEOUT_1MIN
async def swift_generic_exceptions(
    content: str,
    path: str,
) -> Vulnerabilities:
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
) -> List[Awaitable[Vulnerabilities]]:
    coroutines: List[Awaitable[Vulnerabilities]] = []
    content: str

    if file_extension in EXTENSIONS_CSHARP:
        coroutines.append(csharp_insecure_exceptions(
            content=await content_generator(),
            path=path,
        ))
    elif file_extension in EXTENSIONS_JAVA:
        content = await content_generator()
        coroutines.append(java_insecure_exceptions(
            content=content,
            path=path,
        ))
    elif file_extension in EXTENSIONS_PYTHON:
        coroutines.append(python_insecure_exceptions(
            content=await content_generator(),
            path=path,
        ))
    elif file_extension in EXTENSIONS_SWIFT:
        coroutines.append(swift_generic_exceptions(
            content=await content_generator(),
            path=path,
        ))

    return coroutines
