from lib_path.common import (
    EXTENSIONS_CLOUDFORMATION,
    EXTENSIONS_TERRAFORM,
    SHIELD_BLOCKING,
)
from lib_path.f411.cloudformation import (
    cfn_aws_secret_encrypted_without_kms_key,
)
from lib_path.f411.terraform import (
    tfm_aws_secret_encrypted_without_kms_key,
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
def run_cfn_aws_secret_encrypted_without_kms_key(
    content: str, file_ext: str, path: str, template: Any
) -> Vulnerabilities:
    return cfn_aws_secret_encrypted_without_kms_key(
        content=content, file_ext=file_ext, path=path, template=template
    )


@SHIELD_BLOCKING
def run_tfm_aws_secret_encrypted_without_kms_key(
    content: str, path: str, model: Any
) -> Vulnerabilities:
    return tfm_aws_secret_encrypted_without_kms_key(
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

    content = content_generator()
    if file_extension in EXTENSIONS_CLOUDFORMATION:
        for template in load_templates_blocking(content, fmt=file_extension):
            results = (
                *results,
                run_cfn_aws_secret_encrypted_without_kms_key(
                    content, file_extension, path, template
                ),
            )

    elif file_extension in EXTENSIONS_TERRAFORM:
        content = content_generator()
        model = load_terraform(stream=content, default=[])
        results = (
            *results,
            run_tfm_aws_secret_encrypted_without_kms_key(content, path, model),
        )

    return results
