from lib_path.common import (
    EXTENSIONS_JAVA_PROPERTIES,
    SHIELD_BLOCKING,
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


@CACHE_ETERNALLY
@SHIELD_BLOCKING
def run_java_properties_unencrypted_transport(
    content: str, path: str
) -> Vulnerabilities:
    return java_properties_unencrypted_transport(content=content, path=path)


@SHIELD_BLOCKING
def analyze(
    content_generator: Callable[[], str],
    file_extension: str,
    path: str,
    **_: None,
) -> List[Awaitable[Vulnerabilities]]:
    results: List[Awaitable[Vulnerabilities]] = []

    if file_extension in EXTENSIONS_JAVA_PROPERTIES:
        results.append(
            run_java_properties_unencrypted_transport(
                content_generator(), path
            )
        )

    return results
