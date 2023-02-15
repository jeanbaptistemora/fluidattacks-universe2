from collections.abc import (
    Callable,
)
from lib_path.common import (
    EXTENSIONS_CLOUDFORMATION,
    EXTENSIONS_TERRAFORM,
    SHIELD_BLOCKING,
)
from lib_path.f165.cloudformation import (
    cfn_iam_allow_not_action_perms_policies,
    cfn_iam_allow_not_actions_trust_policy,
    cfn_iam_allow_not_principal_trust_policy,
    cfn_iam_allow_not_resource_perms_policies,
    cfn_iam_is_policy_applying_to_users,
)
from lib_path.f165.terraform import (
    tfm_iam_role_is_over_privileged,
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
)


@SHIELD_BLOCKING
def run_cfn_iam_is_policy_applying_to_users(
    content: str, file_ext: str, path: str, template: Any
) -> Vulnerabilities:
    return cfn_iam_is_policy_applying_to_users(
        content=content, file_ext=file_ext, path=path, template=template
    )


@SHIELD_BLOCKING
def run_cfn_iam_allow_not_action_perms_policies(
    content: str, file_ext: str, path: str, template: Any
) -> Vulnerabilities:
    return cfn_iam_allow_not_action_perms_policies(
        content=content, file_ext=file_ext, path=path, template=template
    )


@SHIELD_BLOCKING
def run_cfn_iam_allow_not_resource_perms_policies(
    content: str, file_ext: str, path: str, template: Any
) -> Vulnerabilities:
    return cfn_iam_allow_not_resource_perms_policies(
        content=content, file_ext=file_ext, path=path, template=template
    )


@SHIELD_BLOCKING
def run_cfn_iam_allow_not_actions_trust_policy(
    content: str, file_ext: str, path: str, template: Any
) -> Vulnerabilities:
    return cfn_iam_allow_not_actions_trust_policy(
        content=content, file_ext=file_ext, path=path, template=template
    )


@SHIELD_BLOCKING
def run_cfn_iam_allow_not_principal_trust_policy(
    content: str, file_ext: str, path: str, template: Any
) -> Vulnerabilities:
    return cfn_iam_allow_not_principal_trust_policy(
        content=content, file_ext=file_ext, path=path, template=template
    )


@SHIELD_BLOCKING
def run_tfm_iam_role_is_over_privileged(
    content: str, path: str, model: Any
) -> Vulnerabilities:
    return tfm_iam_role_is_over_privileged(
        content=content, path=path, model=model
    )


@SHIELD_BLOCKING
def analyze(
    content_generator: Callable[[], str],
    file_extension: str,
    path: str,
    **_: None,
) -> tuple[Vulnerabilities, ...]:
    results: tuple[Vulnerabilities, ...] = ()

    content = content_generator()

    if file_extension in EXTENSIONS_CLOUDFORMATION:

        for template in load_templates_blocking(content, fmt=file_extension):
            results = (
                *results,
                run_cfn_iam_allow_not_principal_trust_policy(
                    content, file_extension, path, template
                ),
                run_cfn_iam_allow_not_actions_trust_policy(
                    content, file_extension, path, template
                ),
                run_cfn_iam_allow_not_resource_perms_policies(
                    content, file_extension, path, template
                ),
                run_cfn_iam_allow_not_action_perms_policies(
                    content, file_extension, path, template
                ),
                run_cfn_iam_is_policy_applying_to_users(
                    content, file_extension, path, template
                ),
            )

    elif file_extension in EXTENSIONS_TERRAFORM:
        model = load_terraform(stream=content, default=[])

        results = (
            *results,
            run_tfm_iam_role_is_over_privileged(content, path, model),
        )

    return results
