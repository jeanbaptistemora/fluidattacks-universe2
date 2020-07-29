# Standard library
from itertools import (
    chain,
)
from typing import (
    AsyncGenerator,
    Awaitable,
    Dict,
    List,
    Tuple,
)

# Third party libraries
from pyparsing import (
    Keyword,
    nestedExpr,
    Optional,
)

# Local libraries
from lib_path.common import (
    blocking_get_vulnerabilities,
    C_STYLE_COMMENT,
    EXTENSIONS_CSHARP,
    EXTENSIONS_JAVASCRIPT,
    DOUBLE_QUOTED_STRING,
    SINGLE_QUOTED_STRING,
)
from utils.aio import (
    materialize,
    unblock,
)
from utils.model import (
    FindingEnum,
    Vulnerability,
)


def csharp_insecure_randoms(
    char_to_yx_map: Dict[int, Tuple[int, int]],
    content: str,
    path: str,
) -> Tuple[Vulnerability, ...]:
    # secure versions:
    #  - System.Security.Cryptography.RandomNumberGenerator
    #  - System.Security.Cryptography.RNGCryptoServiceProvider
    grammar = (
        Keyword('new') +
        Optional(Keyword('System') + '.') +
        Keyword('Random') +
        nestedExpr()
    )
    grammar.ignore(C_STYLE_COMMENT)
    grammar.ignore(SINGLE_QUOTED_STRING)
    grammar.ignore(DOUBLE_QUOTED_STRING)

    return blocking_get_vulnerabilities(
        char_to_yx_map=char_to_yx_map,
        content=content,
        finding=FindingEnum.F0034,
        grammar=grammar,
        path=path,
    )


def javascript_insecure_randoms(
    char_to_yx_map: Dict[int, Tuple[int, int]],
    content: str,
    path: str,
) -> Tuple[Vulnerability, ...]:
    grammar = Keyword('Math') + '.' + Keyword('random') + nestedExpr()
    grammar.ignore(C_STYLE_COMMENT)
    grammar.ignore(SINGLE_QUOTED_STRING)
    grammar.ignore(DOUBLE_QUOTED_STRING)

    return blocking_get_vulnerabilities(
        char_to_yx_map=char_to_yx_map,
        content=content,
        finding=FindingEnum.F0034,
        grammar=grammar,
        path=path,
    )


async def analyze(
    char_to_yx_map_generator: AsyncGenerator[Dict[int, Tuple[int, int]], None],
    content_generator: AsyncGenerator[str, None],
    extension: str,
    path: str,
) -> Tuple[Vulnerability, ...]:
    coroutines: List[Awaitable[Tuple[Vulnerability, ...]]] = []

    if extension in EXTENSIONS_CSHARP:
        coroutines.append(unblock(
            csharp_insecure_randoms,
            char_to_yx_map=await char_to_yx_map_generator.__anext__(),
            content=await content_generator.__anext__(),
            path=path,
        ))
    elif extension in EXTENSIONS_JAVASCRIPT:
        coroutines.append(unblock(
            javascript_insecure_randoms,
            char_to_yx_map=await char_to_yx_map_generator.__anext__(),
            content=await content_generator.__anext__(),
            path=path,
        ))

    results: Tuple[Vulnerability, ...] = tuple(chain(*(
        await materialize(coroutines)
    )))

    return results
