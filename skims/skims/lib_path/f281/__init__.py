from lib_path.common import (
    EXTENSIONS_CLOUDFORMATION,
    SHIELD_BLOCKING,
)
from lib_path.f281.cloudformation import (
    cfn_bucket_policy_has_secure_transport,
    cfn_elb2_uses_insecure_port,
)
from model.core_model import (
    Vulnerabilities,
)
from parse_cfn.loader import (
    load_templates_blocking,
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
def run_cfn_bucket_policy_has_secure_transport(
    content: str, path: str, template: Any
) -> Vulnerabilities:
    return cfn_bucket_policy_has_secure_transport(
        content=content, path=path, template=template
    )


@CACHE_ETERNALLY
@SHIELD_BLOCKING
def run_cfn_elb2_uses_insecure_port(
    content: str, file_ext: str, path: str, template: Any
) -> Vulnerabilities:
    return cfn_elb2_uses_insecure_port(
        content=content, file_ext=file_ext, path=path, template=template
    )


@SHIELD_BLOCKING
def analyze(
    content_generator: Callable[[], str],
    file_extension: str,
    path: str,
    **_: None,
) -> List[Awaitable[Vulnerabilities]]:
    coroutines: List[Awaitable[Vulnerabilities]] = []

    if file_extension in EXTENSIONS_CLOUDFORMATION:
        content = content_generator()

        for template in load_templates_blocking(content, fmt=file_extension):
            coroutines.append(
                run_cfn_bucket_policy_has_secure_transport(
                    content, path, template
                )
            )
            coroutines.append(
                run_cfn_elb2_uses_insecure_port(
                    content, file_extension, path, template
                )
            )

    return coroutines
