from lib_path.common import (
    EXTENSIONS_CLOUDFORMATION,
    EXTENSIONS_TERRAFORM,
    SHIELD_BLOCKING,
)
from lib_path.f070.cloudformation import (
    cfn_elb2_target_group_insecure_port,
    cfn_elb2_uses_insecure_security_policy,
)
from lib_path.f070.terraform import (
    tfm_lb_target_group_insecure_port,
)
from model.core_model import (
    Vulnerabilities,
)
from parse_cfn.loader import (
    load_templates_blocking,
)
from parse_hcl2.loader import (
    load_blocking as load_terraform,
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
def run_cfn_elb2_uses_insecure_security_policy(
    content: str, file_ext: str, path: str, template: Any
) -> Vulnerabilities:
    return cfn_elb2_uses_insecure_security_policy(
        content=content, file_ext=file_ext, path=path, template=template
    )


# @CACHE_ETERNALLY
@SHIELD_BLOCKING
def run_cfn_elb2_target_group_insecure_port(
    content: str, file_ext: str, path: str, template: Any
) -> Vulnerabilities:
    return cfn_elb2_target_group_insecure_port(
        content=content, file_ext=file_ext, path=path, template=template
    )


@CACHE_ETERNALLY
@SHIELD_BLOCKING
def run_tfm_lb_target_group_insecure_port(
    content: str, path: str, model: Any
) -> Vulnerabilities:
    return tfm_lb_target_group_insecure_port(
        content=content, path=path, model=model
    )


@SHIELD_BLOCKING
def analyze(
    content_generator: Callable[[], str],
    file_extension: str,
    path: str,
    **_: None,
) -> Tuple[Vulnerabilities, ...]:
    results: Tuple[Vulnerabilities, ...] = ()

    content = content_generator()
    if file_extension in EXTENSIONS_CLOUDFORMATION:
        for template in load_templates_blocking(content, fmt=file_extension):
            results = (
                *results,
                *(
                    fun(content, file_extension, path, template)
                    for fun in (
                        run_cfn_elb2_uses_insecure_security_policy,
                        run_cfn_elb2_target_group_insecure_port,
                    )
                ),
            )

    elif file_extension in EXTENSIONS_TERRAFORM:
        model = load_terraform(stream=content, default=[])

        results = (
            *results,
            *(
                fun(content, path, model)
                for fun in (run_tfm_lb_target_group_insecure_port,)
            ),
        )

    return results
