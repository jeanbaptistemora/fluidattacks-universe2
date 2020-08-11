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
    Keyword,
    MatchFirst,
    Optional,
    nestedExpr,
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
    EXTENSIONS_JAVASCRIPT,
    DOUBLE_QUOTED_STRING,
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
            key='src.lib_path.f061.javascript_swallows_exceptions.description',
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


async def analyze(
    char_to_yx_map_generator: Callable[
        [], Awaitable[Dict[int, Tuple[int, int]]],
    ],
    content_generator: Callable[[], Awaitable[str]],
    file_extension: str,
    path: str,
) -> Tuple[Vulnerability, ...]:
    coroutines: List[Awaitable[Tuple[Vulnerability, ...]]] = []

    if file_extension in EXTENSIONS_JAVASCRIPT:
        coroutines.append(javascript_swallows_exceptions(
            char_to_yx_map=await char_to_yx_map_generator(),
            content=await content_generator(),
            path=path,
        ))

    results: Tuple[Vulnerability, ...] = tuple(chain.from_iterable(
        await collect(coroutines)
    ))

    return results
