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
    MatchFirst,
    Regex,
)

# Third party libraries
from aioextensions import (
    collect,
    unblock_cpu,
)

# Local libraries
from lib_path.common import (
    blocking_get_vulnerabilities,
    HANDLE_ERRORS,
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


async def analyze(
    char_to_yx_map_generator: Callable[
        [], Awaitable[Dict[int, Tuple[int, int]]],
    ],
    content_generator: Callable[[], Awaitable[str]],
    file_extension: str,
    path: str,
) -> Tuple[Vulnerability, ...]:
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
        'yaml',
        'yml',
    }:
        coroutines.append(aws_credentials(
            char_to_yx_map=await char_to_yx_map_generator(),
            content=await content_generator(),
            path=path,
        ))

    results: Tuple[Vulnerability, ...] = tuple(chain.from_iterable(
        await collect(coroutines)
    ))

    return results
