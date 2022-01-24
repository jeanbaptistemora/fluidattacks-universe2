from lib_path.common import (
    EXTENSIONS_CLOUDFORMATION,
    EXTENSIONS_TERRAFORM,
    SHIELD_BLOCKING,
)
from lib_path.f016.cloudformation import (
    cfn_serves_content_over_insecure_protocols,
)
from lib_path.f016.terraform import (
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
from state.cache import (
    CACHE_ETERNALLY,
)
from typing import (
    Any,
    Awaitable,
    Callable,
    List,
)


@CACHE_ETERNALLY
@SHIELD_BLOCKING
def run_cfn_serves_content_over_insecure_protocols(
    content: str, path: str, template: Any
) -> Vulnerabilities:
    return cfn_serves_content_over_insecure_protocols(
        content=content, path=path, template=template
    )


@CACHE_ETERNALLY
@SHIELD_BLOCKING
def run_tfm_aws_serves_content_over_insecure_protocols(
    content: str, path: str, model: Any
) -> Vulnerabilities:
    return tfm_aws_serves_content_over_insecure_protocols(
        content=content, path=path, model=model
    )


@CACHE_ETERNALLY
@SHIELD_BLOCKING
def run_tfm_azure_serves_content_over_insecure_protocols(
    content: str, path: str, model: Any
) -> Vulnerabilities:
    return tfm_azure_serves_content_over_insecure_protocols(
        content=content, path=path, model=model
    )


@SHIELD_BLOCKING
def analyze(
    content_generator: Callable[[], str],
    file_extension: str,
    path: str,
    **_: None,
) -> List[Awaitable[Vulnerabilities]]:
    results: List[Awaitable[Vulnerabilities]] = []

    if file_extension in EXTENSIONS_CLOUDFORMATION:
        content = content_generator()
        for template in load_templates_blocking(content, fmt=file_extension):
            results.append(
                run_cfn_serves_content_over_insecure_protocols(
                    content, path, template
                )
            )

    if file_extension in EXTENSIONS_TERRAFORM:
        content = content_generator()
        model = load_terraform(stream=content, default=[])

        results.append(
            run_tfm_aws_serves_content_over_insecure_protocols(
                content, path, model
            )
        )
        results.append(
            run_tfm_azure_serves_content_over_insecure_protocols(
                content, path, model
            )
        )

    return results
