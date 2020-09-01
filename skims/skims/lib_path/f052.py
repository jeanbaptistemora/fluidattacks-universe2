# Standard library
from typing import (
    Awaitable,
    Callable,
    List,
    Tuple,
)

# Third party libraries
from aioextensions import (
    resolve,
    in_process,
)
from pyparsing import (
    Keyword,
    MatchFirst,
)

# Local libraries
from lib_path.common import (
    blocking_get_vulnerabilities,
    C_STYLE_COMMENT,
    DOUBLE_QUOTED_STRING,
    EXTENSIONS_JAVA,
    SHIELD,
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


def _java_insecure_hash(
    content: str,
    path: str,
) -> Tuple[Vulnerability, ...]:
    grammar = MatchFirst([
        (
            Keyword('MessageDigest') + '.' +
            Keyword('getInstance') + '(' +
            DOUBLE_QUOTED_STRING.copy().addCondition(
                lambda tokens: tokens[0].lower() in {
                    'md2',
                    'md4',
                    'md5',
                    'sha1',
                    'sha-1',
                }
            )
        ),
        (
            Keyword('DigestUtils') + '.' +
            MatchFirst([
                Keyword('getMd2Digest'),
                Keyword('getMd5Digest'),
                Keyword('getShaDigest'),
                Keyword('getSha1Digest'),
                Keyword('md2'),
                Keyword('md2Hex'),
                Keyword('md5'),
                Keyword('md5Hex'),
                Keyword('sha'),
                Keyword('shaHex'),
                Keyword('sha1'),
                Keyword('sha1Hex'),
            ]) + '('
        ),
    ])
    grammar.ignore(C_STYLE_COMMENT)

    return blocking_get_vulnerabilities(
        content=content,
        description=t(
            key='src.lib_path.f052.java_insecure_hash.description',
            path=path,
        ),
        finding=FindingEnum.F052,
        grammar=grammar,
        path=path,
    )


@cache_decorator()
@SHIELD
async def java_insecure_hash(
    content: str,
    path: str,
) -> Tuple[Vulnerability, ...]:
    return await in_process(
        _java_insecure_hash,
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

    if file_extension in EXTENSIONS_JAVA:
        coroutines.append(java_insecure_hash(
            content=await content_generator(),
            path=path,
        ))

    for results in resolve(coroutines, worker_greediness=1):
        for result in await results:
            await store.store(result)
