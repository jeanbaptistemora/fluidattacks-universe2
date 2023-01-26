from lib_path.common import (
    EXTENSIONS_YAML,
    SHIELD_BLOCKING,
)
from lib_path.f134.serverles import (
    severles_cors_wildcard,
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
def run_severles_cors_wildcard(
    content: str, path: str, template: Any
) -> Vulnerabilities:
    return severles_cors_wildcard(
        content=content, path=path, template=template
    )


@SHIELD_BLOCKING
def analyze(
    content_generator: Callable[[], str],
    file_extension: str,
    path: str,
    **_: None,
) -> Tuple[Vulnerabilities, ...]:
    results: Tuple[Vulnerabilities, ...] = ()

    if file_extension in EXTENSIONS_YAML:
        content = content_generator()
        for template in load_templates_blocking(content, fmt=file_extension):
            results = (run_severles_cors_wildcard(content, path, template),)

    return results
