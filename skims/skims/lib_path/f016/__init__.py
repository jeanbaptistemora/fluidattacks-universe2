from lib_path.common import (
    EXTENSIONS_CLOUDFORMATION,
    SHIELD_BLOCKING,
)
from lib_path.f016.cloudformation import (
    cfn_elb_without_sslpolicy,
    cfn_serves_content_over_insecure_protocols,
)
from model.core_model import (
    Vulnerabilities,
)
from parse_cfn.loader import (
    load_templates_blocking,
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

    return results
