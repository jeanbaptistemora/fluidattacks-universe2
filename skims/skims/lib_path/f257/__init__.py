from lib_path.common import (
    EXTENSIONS_CLOUDFORMATION,
    EXTENSIONS_TERRAFORM,
    SHIELD_BLOCKING,
)
from lib_path.f257.cloudformation import (
    cfn_ec2_has_not_termination_protection,
)
from lib_path.f257.terraform import (
    ec2_has_not_termination_protection,
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
def run_cfn_ec2_has_not_termination_protection(
    content: str, file_ext: str, path: str, template: Any
) -> Vulnerabilities:
    return cfn_ec2_has_not_termination_protection(
        content=content, file_ext=file_ext, path=path, template=template
    )


@CACHE_ETERNALLY
@SHIELD_BLOCKING
def run_ec2_has_not_termination_protection(
    content: str, path: str, model: Any
) -> Vulnerabilities:
    return ec2_has_not_termination_protection(
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

    if file_extension in EXTENSIONS_CLOUDFORMATION:
        content = content_generator()
        results = (
            *results,
            *(
                run_cfn_ec2_has_not_termination_protection(
                    content, file_extension, path, template
                )
                for template in load_templates_blocking(
                    content, fmt=file_extension
                )
            ),
        )
    elif file_extension in EXTENSIONS_TERRAFORM:
        content = content_generator()
        model = load_terraform(stream=content, default=[])

        results = (
            *results,
            run_ec2_has_not_termination_protection(content, path, model),
        )

    return results
