# Standard library
from itertools import (
    chain,
)
from typing import (
    Awaitable,
    Callable,
    Dict,
    List,
    Tuple,
)

# Third party libraries
from pyparsing import (
    Empty,
    indentedBlock,
    Keyword,
    LineEnd,
    MatchFirst,
    nestedExpr,
    Optional,
    SkipTo,
)

# Third party libraries
from aioextensions import (
    collect,
    unblock_cpu,
)

# Local libraries
from lib_path.common import (
    blocking_get_vulnerabilities,
    C_STYLE_COMMENT,
    EXTENSIONS_CSHARP,
    EXTENSIONS_JAVA,
    EXTENSIONS_JAVASCRIPT,
    EXTENSIONS_PYTHON,
    DOUBLE_QUOTED_STRING,
    SHARP_STYLE_COMMENT,
    SINGLE_QUOTED_STRING,
)
from state import (
    cache_decorator,
)
from utils.model import (
    FindingEnum,
    Vulnerability,
)
from zone import (
    t,
)


def _csharp_swallows_exceptions(
    char_to_yx_map: Dict[int, Tuple[int, int]],
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
        char_to_yx_map=char_to_yx_map,
        content=content,
        description=t(
            key='src.lib_path.f061.swallows_exceptions.description',
            lang='C#',
            path=path,
        ),
        finding=FindingEnum.F061,
        grammar=grammar,
        path=path,
    )


@cache_decorator()
async def csharp_swallows_exceptions(
    char_to_yx_map: Dict[int, Tuple[int, int]],
    content: str,
    path: str,
) -> Tuple[Vulnerability, ...]:
    return await unblock_cpu(
        _csharp_swallows_exceptions,
        char_to_yx_map=char_to_yx_map,
        content=content,
        path=path,
    )


def _javascript_swallows_exceptions(
    char_to_yx_map: Dict[int, Tuple[int, int]],
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
        char_to_yx_map=char_to_yx_map,
        content=content,
        description=t(
            key='src.lib_path.f061.swallows_exceptions.description',
            lang='Javascript',
            path=path,
        ),
        finding=FindingEnum.F061,
        grammar=grammar,
        path=path,
    )


@cache_decorator()
async def javascript_swallows_exceptions(
    char_to_yx_map: Dict[int, Tuple[int, int]],
    content: str,
    path: str,
) -> Tuple[Vulnerability, ...]:
    return await unblock_cpu(
        _javascript_swallows_exceptions,
        char_to_yx_map=char_to_yx_map,
        content=content,
        path=path,
    )


def _java_swallows_exceptions(
    char_to_yx_map: Dict[int, Tuple[int, int]],
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
        char_to_yx_map=char_to_yx_map,
        content=content,
        description=t(
            key='src.lib_path.f061.swallows_exceptions.description',
            lang='Java',
            path=path,
        ),
        finding=FindingEnum.F061,
        grammar=grammar,
        path=path,
    )


@cache_decorator()
async def java_swallows_exceptions(
    char_to_yx_map: Dict[int, Tuple[int, int]],
    content: str,
    path: str,
) -> Tuple[Vulnerability, ...]:
    return await unblock_cpu(
        _java_swallows_exceptions,
        char_to_yx_map=char_to_yx_map,
        content=content,
        path=path,
    )


def _python_swallows_exceptions(
    char_to_yx_map: Dict[int, Tuple[int, int]],
    content: str,
    path: str,
) -> Tuple[Vulnerability, ...]:
    # Empty() grammar matches 'anything'
    # ~Empty() grammar matches 'not anything' or 'nothing'
    grammar = (
        Keyword('except') +
        SkipTo(LineEnd(), include=True) +
        indentedBlock(Keyword('pass'), indentStack=[1])
    )
    grammar.ignore(SHARP_STYLE_COMMENT)
    grammar.ignore(DOUBLE_QUOTED_STRING)
    grammar.ignore(SINGLE_QUOTED_STRING)

    return blocking_get_vulnerabilities(
        char_to_yx_map=char_to_yx_map,
        content=content,
        description=t(
            key='src.lib_path.f061.swallows_exceptions.description',
            lang='Python',
            path=path,
        ),
        finding=FindingEnum.F061,
        grammar=grammar,
        path=path,
    )


@cache_decorator()
async def python_swallows_exceptions(
    char_to_yx_map: Dict[int, Tuple[int, int]],
    content: str,
    path: str,
) -> Tuple[Vulnerability, ...]:
    return await unblock_cpu(
        _python_swallows_exceptions,
        char_to_yx_map=char_to_yx_map,
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
        coroutines.append(csharp_swallows_exceptions(
            char_to_yx_map=await char_to_yx_map_generator(),
            content=await content_generator(),
            path=path,
        ))
    elif file_extension in EXTENSIONS_JAVA:
        coroutines.append(java_swallows_exceptions(
            char_to_yx_map=await char_to_yx_map_generator(),
            content=await content_generator(),
            path=path,
        ))
    elif file_extension in EXTENSIONS_JAVASCRIPT:
        coroutines.append(javascript_swallows_exceptions(
            char_to_yx_map=await char_to_yx_map_generator(),
            content=await content_generator(),
            path=path,
        ))
    elif file_extension in EXTENSIONS_PYTHON:
        coroutines.append(python_swallows_exceptions(
            char_to_yx_map=await char_to_yx_map_generator(),
            content=await content_generator(),
            path=path,
        ))

    results: Tuple[Vulnerability, ...] = tuple(chain.from_iterable(
        await collect(coroutines)
    ))

    return results
