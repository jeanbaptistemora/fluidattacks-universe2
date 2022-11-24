from lib_path.common import (
    SHIELD_BLOCKING,
)
from lib_path.f236.tsconfig import (
    tsconfig_sourcemap_enabled,
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
def run_tsconfig_sourcemap_enabled(
    content: str, path: str, template: Any
) -> Vulnerabilities:
    return tsconfig_sourcemap_enabled(
        content=content, path=path, template=template
    )


@SHIELD_BLOCKING
def analyze(
    content_generator: Callable[[], str],
    file_extension: str,
    file_name: str,
    path: str,
    **_: None,
) -> Tuple[Vulnerabilities, ...]:
    results: Tuple[Vulnerabilities, ...] = ()
    content = content_generator()

    if file_extension in {"json"} and file_name == "tsconfig":
        for template in load_templates_blocking(content, fmt=file_extension):
            results = (
                *results,
                run_tsconfig_sourcemap_enabled(content, path, template),
            )

    return results
