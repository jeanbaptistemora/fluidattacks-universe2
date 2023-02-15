from collections.abc import (
    Callable,
)
from lib_path.common import (
    SHIELD_BLOCKING,
)
from lib_path.f060.conf_files import (
    allow_acces_from_any_domain,
)
from lib_path.f060.dotnetconfig import (
    has_ssl_disabled,
)
from model.core_model import (
    Vulnerabilities,
)


@SHIELD_BLOCKING
def run_has_ssl_disabled(content: str, path: str) -> Vulnerabilities:
    return has_ssl_disabled(content=content, path=path)


@SHIELD_BLOCKING
def run_allow_acces_from_any_domain(
    content: str,
    path: str,
) -> Vulnerabilities:
    return allow_acces_from_any_domain(content=content, path=path)


@SHIELD_BLOCKING
def analyze(
    content_generator: Callable[[], str],
    file_extension: str,
    path: str,
    **_: None,
) -> tuple[Vulnerabilities, ...]:
    results: tuple[Vulnerabilities, ...] = ()
    content = content_generator()

    if file_extension == "config":
        results = (
            *results,
            run_has_ssl_disabled(content, path),
        )
    if file_extension in ("xml", "jmx"):
        content = content_generator()
        results = (
            *results,
            run_allow_acces_from_any_domain(content, path),
        )

    return results
