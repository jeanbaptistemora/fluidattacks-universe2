from lib_path.common import (
    EXTENSIONS_TERRAFORM,
    SHIELD_BLOCKING,
)
from lib_path.f333.terraform import (
    ec2_has_terminate_shutdown_behavior,
    tfm_ec2_associate_public_ip_address,
)
from model.core_model import (
    Vulnerabilities,
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
def run_ec2_has_terminate_shutdown_behavior(
    content: str, path: str, model: Any
) -> Vulnerabilities:
    return ec2_has_terminate_shutdown_behavior(
        content=content, path=path, model=model
    )


@CACHE_ETERNALLY
@SHIELD_BLOCKING
def run_tfm_ec2_associate_public_ip_address(
    content: str, path: str, model: Any
) -> Vulnerabilities:
    return tfm_ec2_associate_public_ip_address(
        content=content, path=path, model=model
    )


@SHIELD_BLOCKING
def analyze(
    content_generator: Callable[[], str],
    file_extension: str,
    path: str,
    **_: None,
) -> List[Awaitable[Vulnerabilities]]:
    coroutines: List[Awaitable[Vulnerabilities]] = []

    if file_extension in EXTENSIONS_TERRAFORM:
        content = content_generator()
        model = load_terraform(stream=content, default=[])

        coroutines.append(
            run_ec2_has_terminate_shutdown_behavior(content, path, model)
        )
        coroutines.append(
            run_tfm_ec2_associate_public_ip_address(content, path, model)
        )

    return coroutines
