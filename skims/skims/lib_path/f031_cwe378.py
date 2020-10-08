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
)

# Local libraries
from lib_path.common import (
    blocking_get_vulnerabilities,
    C_STYLE_COMMENT,
    DOUBLE_QUOTED_STRING,
    EXTENSIONS_JAVA,
    SHIELD,
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


def _java_file_create_temp_file(
    content: str,
    path: str,
) -> Tuple[Vulnerability, ...]:
    grammar = Keyword('File') + '.' + Keyword('createTempFile') + '('
    grammar.ignore(C_STYLE_COMMENT)
    grammar.ignore(DOUBLE_QUOTED_STRING)
    grammar.ignore(SINGLE_QUOTED_STRING)

    translation_key = (
        'src.lib_path.f031_cwe378.java_file_create_temp_file.description'
    )

    return blocking_get_vulnerabilities(
        content=content,
        cwe={'378'},
        description=t(key=translation_key, path=path),
        finding=FindingEnum.F031_CWE378,
        grammar=grammar,
        path=path,
    )


@cache_decorator()
@SHIELD
async def java_file_create_temp_file(
    content: str,
    path: str,
) -> Tuple[Vulnerability, ...]:
    return await in_process(
        _java_file_create_temp_file,
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
        coroutines.append(java_file_create_temp_file(
            content=await content_generator(),
            path=path,
        ))

    for results in resolve(coroutines, worker_greediness=1):
        for result in await results:
            await store.store(result)
