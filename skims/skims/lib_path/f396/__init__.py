from lib_path.common import (
    EXTENSIONS_CLOUDFORMATION,
    EXTENSIONS_TERRAFORM,
    SHIELD_BLOCKING,
)
from lib_path.f396.cloudformation import (
    cfn_kms_key_is_key_rotation_absent_or_disabled,
)
from lib_path.f396.terraform import (
    tfm_kms_key_is_key_rotation_absent_or_disabled,
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
def run_cfn_kms_key_is_key_rotation_absent_or_disabled(
    content: str, file_ext: str, path: str, template: Any
) -> Vulnerabilities:
    return cfn_kms_key_is_key_rotation_absent_or_disabled(
        content=content, file_ext=file_ext, path=path, template=template
    )


@SHIELD_BLOCKING
def run_tfm_kms_key_is_key_rotation_absent_or_disabled(
    content: str, path: str, model: Any
) -> Vulnerabilities:
    return tfm_kms_key_is_key_rotation_absent_or_disabled(
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
        results = (
            *results,
            *(
                run_cfn_kms_key_is_key_rotation_absent_or_disabled(
                    content, file_extension, path, template
                )
                for template in load_templates_blocking(
                    content, fmt=file_extension
                )
            ),
        )

    elif file_extension in EXTENSIONS_TERRAFORM:
        model = load_terraform(stream=content, default=[])
        results = (
            *results,
            *(
                fun(content, path, model)
                for fun in (
                    run_tfm_kms_key_is_key_rotation_absent_or_disabled,
                )
            ),
        )

    return results
