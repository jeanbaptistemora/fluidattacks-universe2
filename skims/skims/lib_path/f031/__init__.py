from collections.abc import (
    Callable,
)
from lib_path.common import (
    EXTENSIONS_CLOUDFORMATION,
    EXTENSIONS_TERRAFORM,
    SHIELD_BLOCKING,
)
from lib_path.f031.cloudformation import (
    cfn_admin_policy_attached,
    cfn_bucket_policy_allows_public_access,
    cfn_iam_has_full_access_to_ssm,
    cfn_iam_user_missing_role_based_security,
    cfn_negative_statement,
)
from lib_path.f031.terraform import (
    terraform_admin_policy_attached,
    terraform_negative_statement,
    terraform_open_passrole,
    tfm_bucket_policy_allows_public_access,
    tfm_iam_excessive_role_policy,
    tfm_iam_has_full_access_to_ssm,
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
def run_cfn_admin_policy_attached(
    content: str, path: str, template: Any
) -> Vulnerabilities:
    # cfn_nag W43 IAM role should not have AdministratorAccess policy
    return cfn_admin_policy_attached(
        content=content, path=path, template=template
    )


@SHIELD_BLOCKING
def run_cfn_bucket_policy_allows_public_access(
    content: str, path: str, template: Any
) -> Vulnerabilities:
    return cfn_bucket_policy_allows_public_access(
        content=content, path=path, template=template
    )


@SHIELD_BLOCKING
def run_cfn_iam_user_missing_role_based_security(
    content: str, path: str, template: Any
) -> Vulnerabilities:
    return cfn_iam_user_missing_role_based_security(
        content=content, path=path, template=template
    )


@SHIELD_BLOCKING
def run_cfn_negative_statement(
    content: str, path: str, template: Any
) -> Vulnerabilities:
    # cloudconformity IAM-061
    # cfn_nag W14 IAM role should not allow Allow+NotAction on trust perms
    # cfn_nag W15 IAM role should not allow Allow+NotAction
    # cfn_nag W16 IAM policy should not allow Allow+NotAction
    # cfn_nag W17 IAM managed policy should not allow Allow+NotAction
    # cfn_nag W21 IAM role should not allow Allow+NotResource
    # cfn_nag W22 IAM policy should not allow Allow+NotResource
    # cfn_nag W23 IAM managed policy should not allow Allow+NotResource
    return cfn_negative_statement(
        content=content, path=path, template=template
    )


@SHIELD_BLOCKING
def run_cfn_iam_has_full_access_to_ssm(
    content: str, path: str, template: Any
) -> Vulnerabilities:
    return cfn_iam_has_full_access_to_ssm(
        content=content, path=path, template=template
    )


@SHIELD_BLOCKING
def run_terraform_admin_policy_attached(
    content: str, path: str, model: Any
) -> Vulnerabilities:
    # cfn_nag W43 IAM role should not have AdministratorAccess policy
    return terraform_admin_policy_attached(
        content=content, path=path, model=model
    )


@SHIELD_BLOCKING
def run_tfm_bucket_policy_allows_public_access(
    content: str, path: str, model: Any
) -> Vulnerabilities:
    return tfm_bucket_policy_allows_public_access(
        content=content, path=path, model=model
    )


@SHIELD_BLOCKING
def run_tfm_iam_has_full_access_to_ssm(
    content: str, path: str, model: Any
) -> Vulnerabilities:
    return tfm_iam_has_full_access_to_ssm(
        content=content, path=path, model=model
    )


@SHIELD_BLOCKING
def run_tfm_iam_excessive_role_policy(
    content: str, path: str, model: Any
) -> Vulnerabilities:
    return tfm_iam_excessive_role_policy(
        content=content, path=path, model=model
    )


@SHIELD_BLOCKING
def run_terraform_negative_statement(
    content: str, path: str, model: Any
) -> Vulnerabilities:
    # cloudconformity IAM-061
    # cfn_nag W14 IAM role should not allow Allow+NotAction on trust perms
    # cfn_nag W15 IAM role should not allow Allow+NotAction
    # cfn_nag W16 IAM policy should not allow Allow+NotAction
    # cfn_nag W17 IAM managed policy should not allow Allow+NotAction
    # cfn_nag W21 IAM role should not allow Allow+NotResource
    # cfn_nag W22 IAM policy should not allow Allow+NotResource
    # cfn_nag W23 IAM managed policy should not allow Allow+NotResource
    return terraform_negative_statement(
        content=content, path=path, model=model
    )


@SHIELD_BLOCKING
def run_terraform_open_passrole(
    content: str, path: str, model: Any
) -> Vulnerabilities:
    # cfn_nag F38 IAM role should not allow * resource with PassRole action
    #             on its permissions policy
    # cfn_nag F39 IAM policy should not allow * resource with PassRole action
    # cfn_nag F40 IAM managed policy should not allow a * resource with
    #             PassRole action
    return terraform_open_passrole(content=content, path=path, model=model)


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
                *(
                    fun(content, path, template)
                    for fun in (
                        run_cfn_admin_policy_attached,
                        run_cfn_bucket_policy_allows_public_access,
                        run_cfn_iam_user_missing_role_based_security,
                        run_cfn_negative_statement,
                        run_cfn_iam_has_full_access_to_ssm,
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
                    run_terraform_admin_policy_attached,
                    run_tfm_bucket_policy_allows_public_access,
                    run_tfm_iam_excessive_role_policy,
                    run_terraform_negative_statement,
                    run_terraform_open_passrole,
                    run_tfm_iam_has_full_access_to_ssm,
                )
            ),
        )

    return results
