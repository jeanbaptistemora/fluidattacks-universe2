from lib_path.common import (
    EXTENSIONS_CLOUDFORMATION,
    SHIELD_BLOCKING,
)
from lib_path.f044.cloudformation import (
    severless_bucket_has_https_methos_enabled,
)
from lib_path.f044.conf_files import (
    header_allow_all_methods,
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
def run_severless_bucket_has_https_methos_enabled(
    content: str, path: str, template: Any
) -> Vulnerabilities:
    return severless_bucket_has_https_methos_enabled(
        content=content, path=path, template=template
    )


@SHIELD_BLOCKING
def run_header_allow_all_methods(
    content: str,
    path: str,
) -> Vulnerabilities:
    return header_allow_all_methods(content=content, path=path)


@SHIELD_BLOCKING
def analyze(
    content_generator: Callable[[], str],
    file_extension: str,
    path: str,
    **_: None,
) -> Tuple[Vulnerabilities, ...]:
    results: Tuple[Vulnerabilities, ...] = ()

    if file_extension in EXTENSIONS_CLOUDFORMATION:
        content = content_generator()

        for template in load_templates_blocking(content, fmt=file_extension):
            results = (
                *results,
                run_severless_bucket_has_https_methos_enabled(
                    content, path, template
                ),
            )

    if file_extension in ("config", "xml", "jmx"):
        content = content_generator()
        results = (
            *results,
            run_header_allow_all_methods(content, path),
        )
    return results
