from lib_path.common import (
    SHIELD_BLOCKING,
)
from lib_path.f149.conf_files import (
    network_ssl_disabled,
)
from model.core_model import (
    Vulnerabilities,
)
from typing import (
    Callable,
    Tuple,
)


@SHIELD_BLOCKING
def run_network_ssl_disabled(content: str, path: str) -> Vulnerabilities:
    return network_ssl_disabled(content=content, path=path)


@SHIELD_BLOCKING
def analyze(
    content_generator: Callable[[], str],
    file_extension: str,
    path: str,
    **_: None,
) -> Tuple[Vulnerabilities, ...]:
    results: Tuple[Vulnerabilities, ...] = ()

    if file_extension == "config":
        results = (
            *results,
            run_network_ssl_disabled(content_generator(), path),
        )

    return results
