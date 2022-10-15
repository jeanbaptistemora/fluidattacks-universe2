# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from lib_path.common import (
    EXTENSIONS_CLOUDFORMATION,
    EXTENSIONS_JSON,
    EXTENSIONS_TERRAFORM,
    SHIELD_BLOCKING,
)
from lib_path.f325.cloudformation import (
    cfn_iam_has_privileges_over_iam,
    cfn_iam_has_wildcard_resource_on_write_action,
    cfn_iam_is_policy_miss_configured,
    cfn_iam_is_role_over_privileged,
    cfn_kms_key_has_master_keys_exposed_to_everyone,
)
from lib_path.f325.conf_files import (
    json_principal_wildcard,
)
from lib_path.f325.terraform import (
    tfm_iam_has_wildcard_resource_on_write_action,
    tfm_iam_role_is_over_privileged,
    tfm_kms_key_has_master_keys_exposed_to_everyone,
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
def run_cfn_kms_key_has_master_keys_exposed_to_everyone(
    content: str, path: str, template: Any
) -> Vulnerabilities:
    return cfn_kms_key_has_master_keys_exposed_to_everyone(
        content=content, path=path, template=template
    )


@SHIELD_BLOCKING
def run_cfn_iam_has_wildcard_resource_on_write_action(
    content: str, path: str, template: Any
) -> Vulnerabilities:
    return cfn_iam_has_wildcard_resource_on_write_action(
        content=content, path=path, template=template
    )


@SHIELD_BLOCKING
def run_cfn_iam_is_policy_miss_configured(
    content: str,
    file_ext: str,
    path: str,
    template: Any,
) -> Vulnerabilities:
    return cfn_iam_is_policy_miss_configured(
        content=content, file_ext=file_ext, path=path, template=template
    )


@SHIELD_BLOCKING
def run_cfn_iam_has_privileges_over_iam(
    content: str, path: str, template: Any
) -> Vulnerabilities:
    return cfn_iam_has_privileges_over_iam(
        content=content, path=path, template=template
    )


@SHIELD_BLOCKING
def run_cfn_iam_is_role_over_privileged(
    content: str, file_ext: str, path: str, template: Any
) -> Vulnerabilities:
    return cfn_iam_is_role_over_privileged(
        content=content, file_ext=file_ext, path=path, template=template
    )


@SHIELD_BLOCKING
def run_tfm_iam_has_wildcard_resource_on_write_action(
    content: str, path: str, model: Any
) -> Vulnerabilities:
    return tfm_iam_has_wildcard_resource_on_write_action(
        content=content, path=path, model=model
    )


@SHIELD_BLOCKING
def run_tfm_kms_key_has_master_keys_exposed_to_everyone(
    content: str, path: str, model: Any
) -> Vulnerabilities:
    return tfm_kms_key_has_master_keys_exposed_to_everyone(
        content=content, path=path, model=model
    )


@SHIELD_BLOCKING
def run_tfm_iam_role_is_over_privileged(
    content: str, path: str, model: Any
) -> Vulnerabilities:
    return tfm_iam_role_is_over_privileged(
        content=content, path=path, model=model
    )


@SHIELD_BLOCKING
def run_json_principal_wildcard(
    content: str, path: str, template: Any
) -> Vulnerabilities:
    return json_principal_wildcard(
        content=content, path=path, template=template
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
                run_cfn_kms_key_has_master_keys_exposed_to_everyone(
                    content, path, template
                ),
                run_cfn_iam_has_wildcard_resource_on_write_action(
                    content, path, template
                ),
                run_cfn_iam_is_policy_miss_configured(
                    content, file_extension, path, template
                ),
                run_cfn_iam_has_privileges_over_iam(content, path, template),
                run_cfn_iam_is_role_over_privileged(
                    content, file_extension, path, template
                ),
                run_json_principal_wildcard(content, path, template),
            )
            if file_extension in EXTENSIONS_JSON:
                results = (
                    *results,
                    run_json_principal_wildcard(content, path, template),
                )

    elif file_extension in EXTENSIONS_TERRAFORM:
        model = load_terraform(stream=content, default=[])

        results = (
            *results,
            *(
                fun(content, path, model)
                for fun in (
                    run_tfm_kms_key_has_master_keys_exposed_to_everyone,
                    run_tfm_iam_has_wildcard_resource_on_write_action,
                    run_tfm_iam_role_is_over_privileged,
                )
            ),
        )

    return results
