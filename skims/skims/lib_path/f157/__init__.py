from lib_path.common import (
    EXTENSIONS_TERRAFORM,
    SHIELD_BLOCKING,
)
from lib_path.f157.terraform import (
    tfm_azure_kv_default_network_access,
    tfm_azure_sa_default_network_access,
    tfm_azure_unrestricted_access_network_segments,
)
from model.core_model import (
    Vulnerabilities,
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
def run_tfm_azure_unrestricted_access_network_segments(
    content: str, path: str, model: Any
) -> Vulnerabilities:
    return tfm_azure_unrestricted_access_network_segments(
        content=content, path=path, model=model
    )


@SHIELD_BLOCKING
def run_tfm_azure_sa_default_network_access(
    content: str, path: str, model: Any
) -> Vulnerabilities:
    return tfm_azure_sa_default_network_access(
        content=content, path=path, model=model
    )


@SHIELD_BLOCKING
def run_tfm_azure_kv_default_network_access(
    content: str, path: str, model: Any
) -> Vulnerabilities:
    return tfm_azure_kv_default_network_access(
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

    if file_extension in EXTENSIONS_TERRAFORM:
        content = content_generator()
        model = load_terraform(stream=content, default=[])
        results = (
            *results,
            run_tfm_azure_unrestricted_access_network_segments(
                content, path, model
            ),
            run_tfm_azure_sa_default_network_access(content, path, model),
            run_tfm_azure_kv_default_network_access(content, path, model),
        )

    return results
