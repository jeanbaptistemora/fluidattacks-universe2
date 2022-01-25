from lib_path.common import (
    EXTENSIONS_CLOUDFORMATION,
    SHIELD_BLOCKING,
)
from lib_path.f099.cloudformation import (
    cfn_bucket_policy_has_server_side_encryption_disabled,
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
def run_cfn_bucket_policy_has_server_side_encryption_disabled(
    content: str, path: str, template: Any
) -> Vulnerabilities:
    return cfn_bucket_policy_has_server_side_encryption_disabled(
        content=content, path=path, template=template
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
                run_cfn_bucket_policy_has_server_side_encryption_disabled(
                    content, path, template
                )
            )

    return coroutines
