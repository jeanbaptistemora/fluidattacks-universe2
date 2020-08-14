# Standard library
from typing import (
    Awaitable,
    Callable,
    Dict,
    List,
    Tuple,
)

# Third party libraries
from pyparsing import (
    MatchFirst,
    nestedExpr,
    Regex,
)

# Third party libraries
from aioextensions import (
    resolve,
    unblock_cpu,
)

# Local libraries
from lib_path.common import (
    BACKTICK_QUOTED_STRING,
    blocking_get_vulnerabilities,
    DOUBLE_QUOTED_STRING,
    EXTENSIONS_JAVASCRIPT,
    HANDLE_ERRORS,
    SINGLE_QUOTED_STRING,
)
from state.cache import (
    cache_decorator,
)
from state.ephemeral import (
    EphemeralStore,
)
from utils.model import (
    FindingEnum,
    Vulnerability,
)
from zone import (
    t,
)


def _aws_credentials(
    char_to_yx_map: Dict[int, Tuple[int, int]],
    content: str,
    path: str,
) -> Tuple[Vulnerability, ...]:
    grammar = MatchFirst([
        Regex(r'AKIA[A-Z0-9]{16}'),
    ])

    return blocking_get_vulnerabilities(
        char_to_yx_map=char_to_yx_map,
        content=content,
        description=t(
            key='src.lib_path.f009.aws_credentials.description',
            path=path,
        ),
        finding=FindingEnum.F009,
        grammar=grammar,
        path=path,
    )


@cache_decorator()
@HANDLE_ERRORS
async def aws_credentials(
    char_to_yx_map: Dict[int, Tuple[int, int]],
    content: str,
    path: str,
) -> Tuple[Vulnerability, ...]:
    return await unblock_cpu(
        _aws_credentials,
        char_to_yx_map=char_to_yx_map,
        content=content,
        path=path,
    )


# @cache_decorator()
@HANDLE_ERRORS
async def crypto_js_credentials(
    char_to_yx_map: Dict[int, Tuple[int, int]],
    content: str,
    path: str,
) -> Tuple[Vulnerability, ...]:
    return await unblock_cpu(
        _crypto_js_credentials,
        char_to_yx_map=char_to_yx_map,
        content=content,
        path=path,
    )


def _crypto_js_credentials(
    char_to_yx_map: Dict[int, Tuple[int, int]],
    content: str,
    path: str,
) -> Tuple[Vulnerability, ...]:
    grammar = (
        'CryptoJS' + '.' + 'enc' + '.' + MatchFirst({
            'Base64',
            'Utf16',
            'Utf16LE',
            'Hex',
            'Latin1',
            'Utf8',
        }) + '.' + 'parse' + nestedExpr(
            closer=')',
            content=MatchFirst({
                BACKTICK_QUOTED_STRING,
                DOUBLE_QUOTED_STRING,
                SINGLE_QUOTED_STRING,
            }),
            ignoreExpr=None,
            opener='(',
        )
    )

    return blocking_get_vulnerabilities(
        char_to_yx_map=char_to_yx_map,
        content=content,
        description=t(
            key='src.lib_path.f009.crypto_js_credentials.description',
            path=path,
        ),
        finding=FindingEnum.F009,
        grammar=grammar,
        path=path,
    )


async def analyze(
    char_to_yx_map_generator: Callable[
        [], Awaitable[Dict[int, Tuple[int, int]]],
    ],
    content_generator: Callable[[], Awaitable[str]],
    file_extension: str,
    path: str,
    store: EphemeralStore,
) -> None:
    coroutines: List[Awaitable[Tuple[Vulnerability, ...]]] = []

    if file_extension in {
        'groovy',
        'java',
        'jpage',
        'js',
        'json',
        'py',
        'sbt',
        'sql',
        'swift',
        'yaml',
        'yml',
    }:
        coroutines.append(aws_credentials(
            char_to_yx_map=await char_to_yx_map_generator(),
            content=await content_generator(),
            path=path,
        ))

    if file_extension in EXTENSIONS_JAVASCRIPT:
        coroutines.append(crypto_js_credentials(
            char_to_yx_map=await char_to_yx_map_generator(),
            content=await content_generator(),
            path=path,
        ))

    for results in resolve(coroutines, worker_greediness=1):
        for result in await results:
            await store.store(result)
