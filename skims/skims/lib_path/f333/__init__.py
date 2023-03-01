from collections.abc import (
    Callable,
)
from lib_path.common import (
    EXTENSIONS_CLOUDFORMATION,
    SHIELD_BLOCKING,
)
from lib_path.f333.cloudformation import (
    cfn_ec2_associate_public_ip_address,
    cfn_ec2_has_terminate_shutdown_behavior,
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
def run_cfn_ec2_associate_public_ip_address(
    content: str, path: str, template: Any
) -> Vulnerabilities:
    return cfn_ec2_associate_public_ip_address(
        content=content, path=path, template=template
    )


@SHIELD_BLOCKING
def run_cfn_ec2_has_terminate_shutdown_behavior(
    content: str, file_ext: str, path: str, template: Any
) -> Vulnerabilities:
    return cfn_ec2_has_terminate_shutdown_behavior(
        content=content, file_ext=file_ext, path=path, template=template
    )


@SHIELD_BLOCKING
def analyze(
    content_generator: Callable[[], str],
    file_extension: str,
    path: str,
    **_: None,
) -> tuple[Vulnerabilities, ...]:
    results: tuple[Vulnerabilities, ...] = ()

    content = content_generator()
    if file_extension in EXTENSIONS_CLOUDFORMATION:
        for template in load_templates_blocking(content, fmt=file_extension):
            results = (
                run_cfn_ec2_associate_public_ip_address(
                    content, path, template
                ),
                run_cfn_ec2_has_terminate_shutdown_behavior(
                    content, file_extension, path, template
                ),
            )

    return results
