from collections.abc import (
    Callable,
)
from lib_path.common import (
    EXTENSIONS_CLOUDFORMATION,
    SHIELD_BLOCKING,
)
from lib_path.f256.cloudformation import (
    cfn_rds_has_not_automated_backups,
)
from model.core_model import (
    Vulnerabilities,
)
from parse_cfn.loader import (
    load_templates_blocking,
)
from typing import (
    Any,
)


@SHIELD_BLOCKING
def run_cfn_rds_has_not_automated_backups(
    content: str, path: str, template: Any
) -> Vulnerabilities:
    return cfn_rds_has_not_automated_backups(
        content=content, path=path, template=template
    )


@SHIELD_BLOCKING
def analyze(
    content_generator: Callable[[], str],
    file_extension: str,
    path: str,
    **_: None,
) -> tuple[Vulnerabilities, ...]:
    results: tuple[Vulnerabilities, ...] = ()

    if file_extension in EXTENSIONS_CLOUDFORMATION:
        content = content_generator()
        for template in load_templates_blocking(content, fmt=file_extension):
            results = (
                *results,
                run_cfn_rds_has_not_automated_backups(content, path, template),
            )

    return results
