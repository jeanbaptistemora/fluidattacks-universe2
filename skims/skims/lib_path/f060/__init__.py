from lib_path.common import (
    SHIELD_BLOCKING,
)
from lib_path.f060.conf_files import (
    json_allowed_hosts,
)
from lib_path.f060.dotnetconfig import (
    has_ssl_disabled,
)
from model.core_model import (
    Vulnerabilities,
)
from parse_cfn.loader import (
    load_templates_blocking,
)
from typing import (
    Any,
    Callable,
    Tuple,
)


@SHIELD_BLOCKING
def run_has_ssl_disabled(content: str, path: str) -> Vulnerabilities:
    return has_ssl_disabled(content=content, path=path)


@SHIELD_BLOCKING
def run_json_allowed_hosts(
    content: str, path: str, template: Any
) -> Vulnerabilities:
    return json_allowed_hosts(content=content, path=path, template=template)


@SHIELD_BLOCKING
def analyze(
    content_generator: Callable[[], str],
    file_extension: str,
    path: str,
    **_: None,
) -> Tuple[Vulnerabilities, ...]:
    results: Tuple[Vulnerabilities, ...] = ()
    content = content_generator()

    if file_extension == "config":
        results = (
            *results,
            run_has_ssl_disabled(content, path),
        )
    if file_extension in {"json"}:
        for template in load_templates_blocking(content, fmt=file_extension):
            results = (
                *results,
                run_json_allowed_hosts(content, path, template),
            )

    return results
