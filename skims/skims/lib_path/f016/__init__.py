from lib_path.common import (
    EXTENSIONS_CLOUDFORMATION,
    EXTENSIONS_TERRAFORM,
    SHIELD_BLOCKING,
)
from lib_path.f016.cloudformation import (
    cfn_elb_without_sslpolicy,
    cfn_serves_content_over_insecure_protocols,
)
from lib_path.f016.terraform import (
    tfm_aws_elb_without_sslpolicy,
    tfm_aws_serves_content_over_insecure_protocols,
    tfm_azure_serves_content_over_insecure_protocols,
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
    Callable,
    Tuple,
)


@SHIELD_BLOCKING
def run_cfn_serves_content_over_insecure_protocols(
    content: str, path: str, template: Any
) -> Vulnerabilities:
    return cfn_serves_content_over_insecure_protocols(
        content=content, path=path, template=template
    )


@SHIELD_BLOCKING
def run_cfn_elb_without_sslpolicy(
    content: str, path: str, template: Any
) -> Vulnerabilities:
    return cfn_elb_without_sslpolicy(
        content=content, path=path, template=template
    )


@SHIELD_BLOCKING
def run_tfm_aws_serves_content_over_insecure_protocols(
    content: str, path: str, model: Any
) -> Vulnerabilities:
    return tfm_aws_serves_content_over_insecure_protocols(
        content=content, path=path, model=model
    )


@SHIELD_BLOCKING
def run_tfm_azure_serves_content_over_insecure_protocols(
    content: str, path: str, model: Any
) -> Vulnerabilities:
    return tfm_azure_serves_content_over_insecure_protocols(
        content=content, path=path, model=model
    )


@SHIELD_BLOCKING
def run_tfm_aws_elb_without_sslpolicy(
    content: str, path: str, model: Any
) -> Vulnerabilities:
    return tfm_aws_elb_without_sslpolicy(
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
        for template in load_templates_blocking(content, fmt=file_extension):
            results = (
                *results,
                *(
                    fun(content, path, template)
                    for fun in (
                        run_cfn_serves_content_over_insecure_protocols,
                        run_cfn_elb_without_sslpolicy,
                    )
                ),
            )

    if file_extension in EXTENSIONS_TERRAFORM:
        content = content_generator()
        model = load_terraform(stream=content, default=[])
        results = (
            *results,
            run_tfm_aws_serves_content_over_insecure_protocols(
                content, path, model
            ),
            run_tfm_azure_serves_content_over_insecure_protocols(
                content, path, model
            ),
            run_tfm_aws_elb_without_sslpolicy(content, path, model),
        )
    return results
