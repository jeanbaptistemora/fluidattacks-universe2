from lib_path.common import (
    EXTENSIONS_CLOUDFORMATION,
    EXTENSIONS_TERRAFORM,
    SHIELD_BLOCKING,
)
from lib_path.f372.cloudformation import (
    cfn_elb2_uses_insecure_protocol,
    cfn_serves_content_over_http,
)
from lib_path.f372.terraform import (
    tfm_serves_content_over_http,
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
def run_cfn_serves_content_over_http(
    content: str, path: str, template: Any
) -> Vulnerabilities:
    return cfn_serves_content_over_http(
        content=content, path=path, template=template
    )


@SHIELD_BLOCKING
def run_cfn_elb2_uses_insecure_protocol(
    content: str, file_ext: str, path: str, template: Any
) -> Vulnerabilities:
    return cfn_elb2_uses_insecure_protocol(
        content=content, file_ext=file_ext, path=path, template=template
    )


@SHIELD_BLOCKING
def run_tfm_serves_content_over_http(
    content: str, path: str, model: Any
) -> Vulnerabilities:
    return tfm_serves_content_over_http(
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
                run_cfn_serves_content_over_http(content, path, template),
                run_cfn_elb2_uses_insecure_protocol(
                    content, file_extension, path, template
                ),
            )

    if file_extension in EXTENSIONS_TERRAFORM:
        content = content_generator()
        model = load_terraform(stream=content, default=[])
        results = (run_tfm_serves_content_over_http(content, path, model),)

    return results
