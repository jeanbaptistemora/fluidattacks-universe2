from lib_path.common import (
    EXTENSIONS_CLOUDFORMATION,
    EXTENSIONS_TERRAFORM,
    SHIELD_BLOCKING,
)
from lib_path.f250.cloudformation import (
    cfn_ec2_has_unencrypted_volumes,
    cfn_fsx_has_unencrypted_volumes,
)
from lib_path.f250.terraform import (
    tfm_ebs_unencrypted_by_default,
    tfm_ebs_unencrypted_volumes,
    tfm_ec2_unencrypted_volumes,
    tfm_fsx_unencrypted_volumes,
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
def run_cfn_fsx_has_unencrypted_volumes(
    content: str, file_ext: str, path: str, template: Any
) -> Vulnerabilities:
    return cfn_fsx_has_unencrypted_volumes(
        content=content, file_ext=file_ext, path=path, template=template
    )


@SHIELD_BLOCKING
def run_cfn_ec2_has_unencrypted_volumes(
    content: str, file_ext: str, path: str, template: Any
) -> Vulnerabilities:
    return cfn_ec2_has_unencrypted_volumes(
        content=content, file_ext=file_ext, path=path, template=template
    )


@SHIELD_BLOCKING
def run_tfm_fsx_unencrypted_volumes(
    content: str, path: str, model: Any
) -> Vulnerabilities:
    return tfm_fsx_unencrypted_volumes(content=content, path=path, model=model)


@SHIELD_BLOCKING
def run_tfm_ebs_unencrypted_volumes(
    content: str, path: str, model: Any
) -> Vulnerabilities:
    return tfm_ebs_unencrypted_volumes(content=content, path=path, model=model)


@SHIELD_BLOCKING
def run_tfm_ec2_unencrypted_volumes(
    content: str, path: str, model: Any
) -> Vulnerabilities:
    return tfm_ec2_unencrypted_volumes(content=content, path=path, model=model)


@SHIELD_BLOCKING
def run_tfm_ebs_unencrypted_by_default(
    content: str, path: str, model: Any
) -> Vulnerabilities:
    return tfm_ebs_unencrypted_by_default(
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
                *(
                    fun(content, file_extension, path, template)
                    for fun in (
                        run_cfn_fsx_has_unencrypted_volumes,
                        run_cfn_ec2_has_unencrypted_volumes,
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
                    run_tfm_fsx_unencrypted_volumes,
                    run_tfm_ebs_unencrypted_volumes,
                    run_tfm_ec2_unencrypted_volumes,
                    run_tfm_ebs_unencrypted_by_default,
                )
            ),
        )

    return results
