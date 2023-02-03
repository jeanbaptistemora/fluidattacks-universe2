from lib_path.common import (
    EXTENSIONS_CLOUDFORMATION,
    SHIELD_BLOCKING,
)
from lib_path.f246.cloudformation import (
    cfn_rds_has_unencrypted_storage,
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
def run_cfn_rds_has_unencrypted_storage(
    content: str, file_ext: str, path: str, template: Any
) -> Vulnerabilities:
    return cfn_rds_has_unencrypted_storage(
        content=content, file_ext=file_ext, path=path, template=template
    )


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

        results = (
            *results,
            *(
                run_cfn_rds_has_unencrypted_storage(
                    content, file_extension, path, template
                )
                for template in load_templates_blocking(
                    content, fmt=file_extension
                )
            ),
        )

    return results
