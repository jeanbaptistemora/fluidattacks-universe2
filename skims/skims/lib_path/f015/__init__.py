from lib_path.common import (
    EXTENSIONS_TERRAFORM,
    SHIELD_BLOCKING,
)
from lib_path.f015.conf_files import (
    basic_auth_method,
    jmx_header_basic,
)
from lib_path.f015.terraform import (
    tfm_azure_linux_vm_insecure_authentication,
)
from model.core_model import (
    Vulnerabilities,
)
from parse_hcl2.loader import (
    load_blocking as load_terraform_blocking,
)
from typing import (
    Any,
    Callable,
    Tuple,
)


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
def run_jmx_header_basic(
    content: str,
    path: str,
) -> Vulnerabilities:
    return jmx_header_basic(
        content=content,
        path=path,
    )


@SHIELD_BLOCKING
def run_basic_auth_method(content: str, path: str) -> Vulnerabilities:
    return basic_auth_method(content=content, path=path)


@SHIELD_BLOCKING
def analyze(
    content_generator: Callable[[], str],
    file_extension: str,
    path: str,
    **_: None,
) -> Tuple[Vulnerabilities, ...]:
    results: Tuple[Vulnerabilities, ...] = ()

    if file_extension in EXTENSIONS_TERRAFORM:
        content = content_generator()
        model = load_terraform_blocking(stream=content, default=[])
        results = (
            *results,
            run_tfm_azure_linux_vm_insecure_authentication(
                content, path, model
            ),
        )
    elif file_extension in ("config", "xml", "jmx"):
        content = content_generator()
        results = (
            *results,
            run_jmx_header_basic(content, path),
            run_basic_auth_method(content, path),
        )

    return results
