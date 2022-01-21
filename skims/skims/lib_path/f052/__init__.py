from aioextensions import (
    in_process,
)
from lib_path.common import (
    EXTENSIONS_JAVA_PROPERTIES,
    SHIELD,
)
from lib_path.f052.java import (
    java_properties_missing_ssl,
    java_properties_weak_cipher_suite,
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
async def run_java_properties_missing_ssl(
    content: str, path: str
) -> Vulnerabilities:
    return await in_process(
        java_properties_missing_ssl,
        content=content,
        path=path,
    )


@CACHE_ETERNALLY
@SHIELD
@TIMEOUT_1MIN
async def run_java_properties_weak_cipher_suite(
    content: str, path: str
) -> Vulnerabilities:
    return await in_process(
        java_properties_weak_cipher_suite,
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
        content = content_generator()

        coroutines.append(run_java_properties_missing_ssl(content, path))
        coroutines.append(run_java_properties_weak_cipher_suite(content, path))

    return coroutines
