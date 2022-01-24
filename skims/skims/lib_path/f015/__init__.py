from lib_path.common import (
    EXTENSIONS_TERRAFORM,
    SHIELD_BLOCKING,
)
from lib_path.f015.terraform import (
    tfm_azure_linux_vm_insecure_authentication,
    tfm_azure_virtual_machine_insecure_authentication,
)
from model.core_model import (
    Vulnerabilities,
)
from parse_hcl2.loader import (
    load_blocking as load_terraform_blocking,
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
def run_tfm_azure_virtual_machine_insecure_authentication(
    content: str, path: str, model: Any
) -> Vulnerabilities:
    return tfm_azure_virtual_machine_insecure_authentication(
        content=content, path=path, model=model
    )


@CACHE_ETERNALLY
@SHIELD_BLOCKING
def run_tfm_azure_linux_vm_insecure_authentication(
    content: str, path: str, model: Any
) -> Vulnerabilities:
    return tfm_azure_linux_vm_insecure_authentication(
        content=content,
        path=path,
        model=model,
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
        model = load_terraform_blocking(stream=content, default=[])

        coroutines.append(
            run_tfm_azure_virtual_machine_insecure_authentication(
                content, path, model
            )
        )
        coroutines.append(
            run_tfm_azure_linux_vm_insecure_authentication(
                content, path, model
            )
        )

    return coroutines
