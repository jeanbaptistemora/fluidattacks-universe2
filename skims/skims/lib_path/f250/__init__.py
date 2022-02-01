from lib_path.common import (
    EXTENSIONS_CLOUDFORMATION,
    SHIELD_BLOCKING,
)
from lib_path.f250.cloudformation import (
    cfn_ec2_has_unencrypted_volumes,
    cfn_fsx_has_unencrypted_volumes,
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
def run_cfn_fsx_has_unencrypted_volumes(
    content: str, file_ext: str, path: str, template: Any
) -> Vulnerabilities:
    return cfn_fsx_has_unencrypted_volumes(
        content=content, file_ext=file_ext, path=path, template=template
    )


@CACHE_ETERNALLY
@SHIELD_BLOCKING
def run_cfn_ec2_has_unencrypted_volumes(
    content: str, file_ext: str, path: str, template: Any
) -> Vulnerabilities:
    return cfn_ec2_has_unencrypted_volumes(
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

        for template in load_templates_blocking(content, fmt=file_extension):
            results = (
                *results,
                run_cfn_fsx_has_unencrypted_volumes(
                    content, file_extension, path, template
                ),
                run_cfn_ec2_has_unencrypted_volumes(
                    content, file_extension, path, template
                ),
            )

    return results
