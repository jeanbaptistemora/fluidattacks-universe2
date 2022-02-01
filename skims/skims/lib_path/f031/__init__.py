from lib_path.common import (
    EXTENSIONS_CLOUDFORMATION,
    EXTENSIONS_TERRAFORM,
    SHIELD_BLOCKING,
)
from lib_path.f031.cloudformation import (
    cfn_admin_policy_attached,
    cfn_bucket_policy_allows_public_access,
    cfn_ec2_has_not_an_iam_instance_profile,
    cfn_iam_has_full_access_to_ssm,
    cfn_iam_user_missing_role_based_security,
    cfn_negative_statement,
    cfn_open_passrole,
    cfn_permissive_policy,
)
from lib_path.f031.terraform import (
    terraform_admin_policy_attached,
    terraform_negative_statement,
    terraform_open_passrole,
    terraform_permissive_policy,
    tfm_ec2_has_not_an_iam_instance_profile,
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
def run_cfn_admin_policy_attached(
    content: str, path: str, template: Any
) -> Vulnerabilities:
    # cfn_nag W43 IAM role should not have AdministratorAccess policy
    return cfn_admin_policy_attached(
        content=content, path=path, template=template
    )


@CACHE_ETERNALLY
@SHIELD_BLOCKING
def run_cfn_bucket_policy_allows_public_access(
    content: str, path: str, template: Any
) -> Vulnerabilities:
    return cfn_bucket_policy_allows_public_access(
        content=content, path=path, template=template
    )


@CACHE_ETERNALLY
@SHIELD_BLOCKING
def run_cfn_iam_user_missing_role_based_security(
    content: str, path: str, template: Any
) -> Vulnerabilities:
    return cfn_iam_user_missing_role_based_security(
        content=content, path=path, template=template
    )


@CACHE_ETERNALLY
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


@CACHE_ETERNALLY
@SHIELD_BLOCKING
def run_cfn_open_passrole(
    content: str, path: str, template: Any
) -> Vulnerabilities:
    # cfn_nag F38 IAM role should not allow * resource with PassRole action
    #             on its permissions policy
    # cfn_nag F39 IAM policy should not allow * resource with PassRole action
    # cfn_nag F40 IAM managed policy should not allow a * resource with
    #             PassRole action
    return cfn_open_passrole(content=content, path=path, template=template)


@CACHE_ETERNALLY
@SHIELD_BLOCKING
def run_cfn_permissive_policy(
    content: str, path: str, template: Any
) -> Vulnerabilities:
    # cloudconformity IAM-045
    # cloudconformity IAM-049
    # cfn_nag W11 IAM role should not allow * resource on its permissions pol
    # cfn_nag W12 IAM policy should not allow * resource
    # cfn_nag W13 IAM managed policy should not allow * resource
    # cfn_nag F2 IAM role should not allow * action on its trust policy
    # cfn_nag F3 IAM role should not allow * action on its permissions policy
    # cfn_nag F4 IAM policy should not allow * action
    # cfn_nag F5 IAM managed policy should not allow * action
    return cfn_permissive_policy(content=content, path=path, template=template)


@CACHE_ETERNALLY
@SHIELD_BLOCKING
def run_cfn_ec2_has_not_an_iam_instance_profile(
    content: str, file_ext: str, path: str, template: Any
) -> Vulnerabilities:
    return cfn_ec2_has_not_an_iam_instance_profile(
        content=content, file_ext=file_ext, path=path, template=template
    )


@CACHE_ETERNALLY
@SHIELD_BLOCKING
def run_cfn_iam_has_full_access_to_ssm(
    content: str, path: str, template: Any
) -> Vulnerabilities:
    return cfn_iam_has_full_access_to_ssm(
        content=content, path=path, template=template
    )


@CACHE_ETERNALLY
@SHIELD_BLOCKING
def run_terraform_admin_policy_attached(
    content: str, path: str, model: Any
) -> Vulnerabilities:
    # cfn_nag W43 IAM role should not have AdministratorAccess policy
    return terraform_admin_policy_attached(
        content=content, path=path, model=model
    )


@CACHE_ETERNALLY
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


@CACHE_ETERNALLY
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


@CACHE_ETERNALLY
@SHIELD_BLOCKING
def run_terraform_permissive_policy(
    content: str, path: str, model: Any
) -> Vulnerabilities:
    # cloudconformity IAM-045
    # cloudconformity IAM-049
    # cfn_nag W11 IAM role should not allow * resource on its permissions pol
    # cfn_nag W12 IAM policy should not allow * resource
    # cfn_nag W13 IAM managed policy should not allow * resource
    # cfn_nag F2 IAM role should not allow * action on its trust policy
    # cfn_nag F3 IAM role should not allow * action on its permissions policy
    # cfn_nag F4 IAM policy should not allow * action
    # cfn_nag F5 IAM managed policy should not allow * action
    return terraform_permissive_policy(content=content, path=path, model=model)


@CACHE_ETERNALLY
@SHIELD_BLOCKING
def run_tfm_ec2_has_not_an_iam_instance_profile(
    content: str, path: str, model: Any
) -> Vulnerabilities:
    return tfm_ec2_has_not_an_iam_instance_profile(
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
                    fun(content, path, template)
                    for fun in (
                        run_cfn_admin_policy_attached,
                        run_cfn_bucket_policy_allows_public_access,
                        run_cfn_iam_user_missing_role_based_security,
                        run_cfn_negative_statement,
                        run_cfn_open_passrole,
                        run_cfn_permissive_policy,
                        run_cfn_iam_has_full_access_to_ssm,
                    )
                ),
            )
            results = (
                *results,
                run_cfn_ec2_has_not_an_iam_instance_profile(
                    content, file_extension, path, template
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
                    run_terraform_negative_statement,
                    run_terraform_open_passrole,
                    run_terraform_permissive_policy,
                    run_tfm_ec2_has_not_an_iam_instance_profile,
                )
            ),
        )

    return results
