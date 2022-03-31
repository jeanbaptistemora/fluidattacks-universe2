from lib_path.common import (
    EXTENSIONS_TERRAFORM,
    SHIELD_BLOCKING,
)
from lib_path.f411.terraform import (
    tfm_aws_secret_encrypted_whitouth_kms_cmk,
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
    Callable,
    Tuple,
)


@CACHE_ETERNALLY
@SHIELD_BLOCKING
def run_tfm_aws_secret_encrypted_whitouth_kms_cmk(
    content: str, path: str, model: Any
) -> Vulnerabilities:
    return tfm_aws_secret_encrypted_whitouth_kms_cmk(
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
            run_tfm_aws_secret_encrypted_whitouth_kms_cmk(
                content, path, model
            ),
        )

    return results
