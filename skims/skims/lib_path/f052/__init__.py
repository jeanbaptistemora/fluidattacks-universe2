from lib_path.common import (
    EXTENSIONS_JAVA_PROPERTIES,
    SHIELD_BLOCKING,
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


@CACHE_ETERNALLY
@SHIELD_BLOCKING
def run_java_properties_missing_ssl(
    content: str, path: str
) -> Vulnerabilities:
    return java_properties_missing_ssl(content=content, path=path)


@CACHE_ETERNALLY
@SHIELD_BLOCKING
def run_java_properties_weak_cipher_suite(
    content: str, path: str
) -> Vulnerabilities:
    return java_properties_weak_cipher_suite(content=content, path=path)


@SHIELD_BLOCKING
def analyze(
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
