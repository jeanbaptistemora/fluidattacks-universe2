from collections.abc import (
    Callable,
)
from lib_path.common import (
    EXTENSIONS_CLOUDFORMATION,
    EXTENSIONS_TERRAFORM,
    SHIELD_BLOCKING,
)
from lib_path.f281.cloudformation import (
    cfn_bucket_policy_has_secure_transport,
)
from lib_path.f281.terraform import (
    tfm_bucket_policy_has_secure_transport,
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
from typing import (
    Any,
)


@SHIELD_BLOCKING
def run_cfn_bucket_policy_has_secure_transport(
    content: str, path: str, template: Any
) -> Vulnerabilities:
    return cfn_bucket_policy_has_secure_transport(
        content=content, path=path, template=template
    )


@SHIELD_BLOCKING
def run_tfm_bucket_policy_has_secure_transport(
    content: str, path: str, model: Any
) -> Vulnerabilities:
    return tfm_bucket_policy_has_secure_transport(
        content=content, path=path, model=model
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
                run_cfn_bucket_policy_has_secure_transport(
                    content, path, template
                ),
            )

    elif file_extension in EXTENSIONS_TERRAFORM:
        model = load_terraform(stream=content, default=[])

        results = (
            *results,
            *(
                fun(content, path, model)
                for fun in (run_tfm_bucket_policy_has_secure_transport,)
            ),
        )

    return results
