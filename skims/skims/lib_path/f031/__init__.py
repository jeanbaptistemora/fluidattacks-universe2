from collections.abc import (
    Callable,
)
from lib_path.common import (
    EXTENSIONS_CLOUDFORMATION,
    SHIELD_BLOCKING,
)
from lib_path.f031.cloudformation import (
    cfn_admin_policy_attached,
    cfn_bucket_policy_allows_public_access,
    cfn_iam_has_full_access_to_ssm,
    cfn_iam_user_missing_role_based_security,
    cfn_negative_statement,
)
from model.core_model import (
    Vulnerabilities,
)
from parse_cfn.loader import (
    load_templates_blocking,
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

    return results
