from collections.abc import (
    Callable,
)
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
) -> tuple[Vulnerabilities, ...]:
    results: tuple[Vulnerabilities, ...] = ()

    if file_extension in EXTENSIONS_JAVA_PROPERTIES:
        results = (
            *results,
            run_java_properties_unencrypted_transport(
                content_generator(), path
            ),
        )

    return results
