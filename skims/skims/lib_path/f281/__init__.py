from lib_path.common import (
    EXTENSIONS_CLOUDFORMATION,
    SHIELD_BLOCKING,
)
from lib_path.f281.cloudformation import (
    cfn_bucket_policy_has_secure_transport,
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
def run_cfn_bucket_policy_has_secure_transport(
    content: str, path: str, template: Any
) -> Vulnerabilities:
    return cfn_bucket_policy_has_secure_transport(
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
                run_cfn_bucket_policy_has_secure_transport(
                    content, path, template
                ),
            )

    return results
