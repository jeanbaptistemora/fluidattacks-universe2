from lib_path.common import (
    EXTENSIONS_CLOUDFORMATION,
    SHIELD_BLOCKING,
)
from lib_path.f396.cloudformation import (
    cfn_kms_key_is_key_rotation_absent_or_disabled,
)
from model.core_model import (
    Vulnerabilities,
)
from parse_cfn.loader import (
    load_templates_blocking,
)
from state.cache import (
    CACHE_ETERNALLY,
)
from typing import (
    Any,
    Callable,
    Tuple,
)


@CACHE_ETERNALLY
@SHIELD_BLOCKING
def run_cfn_kms_key_is_key_rotation_absent_or_disabled(
    content: str, file_ext: str, path: str, template: Any
) -> Vulnerabilities:
    return cfn_kms_key_is_key_rotation_absent_or_disabled(
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
                run_cfn_kms_key_is_key_rotation_absent_or_disabled(
                    content, file_extension, path, template
                )
                for template in load_templates_blocking(
                    content, fmt=file_extension
                )
            ),
        )

    return results
