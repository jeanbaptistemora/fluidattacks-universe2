# Standard library
import ast
from itertools import (
    chain,
)
from typing import (
    Awaitable,
    Callable,
    Dict,
    Iterator,
    List,
    Set,
    Tuple,
)

# Third party libraries
from aioextensions import (
    collect,
    unblock_cpu,
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
    C_STYLE_COMMENT,
    DOUBLE_QUOTED_STRING,
    EXTENSIONS_CSHARP,
    EXTENSIONS_JAVA,
    EXTENSIONS_PYTHON,
    HANDLE_ERRORS,
    SINGLE_QUOTED_STRING,
    VAR_ATTR_JAVA,
)
from state.cache import (
    cache_decorator,
)
from utils.ast import (
    iterate_nodes,
)
from utils.model import (
    FindingEnum,
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


def _csharp_insecure_exceptions(
    char_to_yx_map: Dict[int, Tuple[int, int]],
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
        char_to_yx_map=char_to_yx_map,
        content=content,
        description=t(
            key='src.lib_path.f060.insecure_exceptions.description',
            lang='C#',
            path=path,
        ),
        finding=FindingEnum.F060,
        grammar=grammar,
        path=path,
    )


@cache_decorator()
@HANDLE_ERRORS
async def csharp_insecure_exceptions(
    char_to_yx_map: Dict[int, Tuple[int, int]],
    content: str,
    path: str,
) -> Tuple[Vulnerability, ...]:
    return await unblock_cpu(
        _csharp_insecure_exceptions,
        char_to_yx_map=char_to_yx_map,
        content=content,
        path=path,
    )


def _java_insecure_exceptions(
    char_to_yx_map: Dict[int, Tuple[int, int]],
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
        char_to_yx_map=char_to_yx_map,
        content=content,
        description=t(
            key='src.lib_path.f060.insecure_exceptions.description',
            lang='Java',
            path=path,
        ),
        finding=FindingEnum.F060,
        grammar=grammar,
        path=path,
    )


@cache_decorator()
@HANDLE_ERRORS
async def java_insecure_exceptions(
    char_to_yx_map: Dict[int, Tuple[int, int]],
    content: str,
    path: str,
) -> Tuple[Vulnerability, ...]:
    return await unblock_cpu(
        _java_insecure_exceptions,
        char_to_yx_map=char_to_yx_map,
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

    return tuple(
        Vulnerability(
            finding=FindingEnum.F060,
            kind=VulnerabilityKindEnum.LINES,
            state=VulnerabilityStateEnum.OPEN,
            what=path,
            where=f'{node.lineno}',
            skims_metadata=SkimsVulnerabilityMetadata(
                description=t(
                    key='src.lib_path.f060.insecure_exceptions.description',
                    lang='Python',
                    path=path,
                ),
                snippet=blocking_to_snippet(
                    column=node.col_offset,
                    content=content,
                    line=node.lineno,
                )
            )
        )
        for node in vulnerable_nodes
    )


@cache_decorator()
async def python_insecure_exceptions(
    content: str,
    path: str,
) -> Tuple[Vulnerability, ...]:
    return await unblock_cpu(
        _python_insecure_exceptions,
        content=content,
        path=path,
    )


async def analyze(
    char_to_yx_map_generator: Callable[
        [], Awaitable[Dict[int, Tuple[int, int]]],
    ],
    content_generator: Callable[[], Awaitable[str]],
    file_extension: str,
    path: str,
) -> Tuple[Vulnerability, ...]:
    coroutines: List[Awaitable[Tuple[Vulnerability, ...]]] = []

    if file_extension in EXTENSIONS_CSHARP:
        coroutines.append(csharp_insecure_exceptions(
            char_to_yx_map=await char_to_yx_map_generator(),
            content=await content_generator(),
            path=path,
        ))
    elif file_extension in EXTENSIONS_JAVA:
        coroutines.append(java_insecure_exceptions(
            char_to_yx_map=await char_to_yx_map_generator(),
            content=await content_generator(),
            path=path,
        ))
    elif file_extension in EXTENSIONS_PYTHON:
        coroutines.append(python_insecure_exceptions(
            content=await content_generator(),
            path=path,
        ))

    results: Tuple[Vulnerability, ...] = tuple(chain.from_iterable(
        await collect(coroutines)
    ))

    return results
