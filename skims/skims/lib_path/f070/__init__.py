from collections.abc import (
    Callable,
)
from lib_path.common import (
    EXTENSIONS_CLOUDFORMATION,
    SHIELD_BLOCKING,
)
from lib_path.f070.cloudformation import (
    cfn_elb2_target_group_insecure_port,
    cfn_elb2_uses_insecure_security_policy,
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
def run_cfn_elb2_uses_insecure_security_policy(
    content: str, path: str, template: Any
) -> Vulnerabilities:
    return cfn_elb2_uses_insecure_security_policy(
        content=content, path=path, template=template
    )


@SHIELD_BLOCKING
def run_cfn_elb2_target_group_insecure_port(
    content: str, file_ext: str, path: str, template: Any
) -> Vulnerabilities:
    return cfn_elb2_target_group_insecure_port(
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
                *results,
                *(
                    fun(content, path, template)
                    for fun in (run_cfn_elb2_uses_insecure_security_policy,)
                ),
                *(
                    fun(content, file_extension, path, template)
                    for fun in (run_cfn_elb2_target_group_insecure_port,)
                ),
            )

    return results
