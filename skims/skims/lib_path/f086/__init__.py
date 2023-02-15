from collections.abc import (
    Callable,
)
from lib_path.common import (
    SHIELD_BLOCKING,
)
from lib_path.f086.html import (
    has_not_subresource_integrity,
)
from model.core_model import (
    Vulnerabilities,
)


@SHIELD_BLOCKING
def run_has_not_subresource_integrity(
    content: str, path: str
) -> Vulnerabilities:
    return has_not_subresource_integrity(content=content, path=path)


@SHIELD_BLOCKING
def analyze(
    content_generator: Callable[[], str],
    file_extension: str,
    path: str,
    **_: None,
) -> tuple[Vulnerabilities, ...]:
    results: tuple[Vulnerabilities, ...] = ()

    if file_extension == "html":
        results = (
            *results,
            run_has_not_subresource_integrity(content_generator(), path),
        )

    return results
