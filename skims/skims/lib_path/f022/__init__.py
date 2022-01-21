from aioextensions import (
    in_process,
)
from lib_path.common import (
    EXTENSIONS_JAVA_PROPERTIES,
    SHIELD,
)
from lib_path.f022.java import (
    java_properties_unencrypted_transport,
)
from model.core_model import (
    Vulnerabilities,
)
from state.cache import (
    CACHE_ETERNALLY,
)
from typing import (
    Awaitable,
    Callable,
    List,
)
from utils.function import (
    TIMEOUT_1MIN,
)


@CACHE_ETERNALLY
@SHIELD
@TIMEOUT_1MIN
async def run_java_properties_unencrypted_transport(
    content: str, path: str
) -> Vulnerabilities:
    return await in_process(
        java_properties_unencrypted_transport,
        content=content,
        path=path,
    )


@SHIELD
async def analyze(
    content_generator: Callable[[], str],
    file_extension: str,
    path: str,
    **_: None,
) -> List[Awaitable[Vulnerabilities]]:
    coroutines: List[Awaitable[Vulnerabilities]] = []

    if file_extension in EXTENSIONS_JAVA_PROPERTIES:
        coroutines.append(
            run_java_properties_unencrypted_transport(
                content_generator(), path
            )
        )

    return coroutines
