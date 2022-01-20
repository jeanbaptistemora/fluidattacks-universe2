from aioextensions import (
    in_process,
)
from lib_path.common import (
    EXTENSIONS_CLOUDFORMATION,
    EXTENSIONS_TERRAFORM,
    SHIELD,
)
from lib_path.f031.cloudformation import (
    cfn_admin_policy_attached,
    cfn_bucket_policy_allows_public_access,
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
)
from model.core_model import (
    Vulnerabilities,
)
from parse_cfn.loader import (
    load_templates,
)
from parse_hcl2.loader import (
    load as load_terraform,
)
from state.cache import (
    CACHE_ETERNALLY,
)
from typing import (
    Any,
    Awaitable,
    Callable,
    List,
)
from utils.function import (
    TIMEOUT_1MIN,
)


@CACHE_ETERNALLY
@SHIELD
@TIMEOUT_1MIN
async def run_cfn_admin_policy_attached(
    content: str, path: str, template: Any
) -> Vulnerabilities:
    # cfn_nag W43 IAM role should not have AdministratorAccess policy
    return await in_process(
        cfn_admin_policy_attached,
        content=content,
        path=path,
        template=template,
    )


@CACHE_ETERNALLY
@SHIELD
@TIMEOUT_1MIN
async def run_cfn_bucket_policy_allows_public_access(
    content: str, path: str, template: Any
) -> Vulnerabilities:
    return await in_process(
        cfn_bucket_policy_allows_public_access,
        content=content,
        path=path,
        template=template,
    )


@CACHE_ETERNALLY
@SHIELD
@TIMEOUT_1MIN
async def run_cfn_iam_user_missing_role_based_security(
    content: str, path: str, template: Any
) -> Vulnerabilities:
    return await in_process(
        cfn_iam_user_missing_role_based_security,
        content=content,
        path=path,
        template=template,
    )


@CACHE_ETERNALLY
@SHIELD
@TIMEOUT_1MIN
async def run_cfn_negative_statement(
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
    return await in_process(
        cfn_negative_statement,
        content=content,
        path=path,
        template=template,
    )


@CACHE_ETERNALLY
@SHIELD
@TIMEOUT_1MIN
async def run_cfn_open_passrole(
    content: str, path: str, template: Any
) -> Vulnerabilities:
    # cfn_nag F38 IAM role should not allow * resource with PassRole action
    #             on its permissions policy
    # cfn_nag F39 IAM policy should not allow * resource with PassRole action
    # cfn_nag F40 IAM managed policy should not allow a * resource with
    #             PassRole action
    return await in_process(
        cfn_open_passrole,
        content=content,
        path=path,
        template=template,
    )


@CACHE_ETERNALLY
@SHIELD
@TIMEOUT_1MIN
async def run_cfn_permissive_policy(
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
    return await in_process(
        cfn_permissive_policy,
        content=content,
        path=path,
        template=template,
    )


@CACHE_ETERNALLY
@SHIELD
@TIMEOUT_1MIN
async def run_terraform_admin_policy_attached(
    content: str, path: str, model: Any
) -> Vulnerabilities:
    # cfn_nag W43 IAM role should not have AdministratorAccess policy
    return await in_process(
        terraform_admin_policy_attached,
        content=content,
        path=path,
        model=model,
    )


@CACHE_ETERNALLY
@SHIELD
@TIMEOUT_1MIN
async def run_terraform_negative_statement(
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
    return await in_process(
        terraform_negative_statement,
        content=content,
        path=path,
        model=model,
    )


@CACHE_ETERNALLY
@SHIELD
@TIMEOUT_1MIN
async def run_terraform_open_passrole(
    content: str, path: str, model: Any
) -> Vulnerabilities:
    # cfn_nag F38 IAM role should not allow * resource with PassRole action
    #             on its permissions policy
    # cfn_nag F39 IAM policy should not allow * resource with PassRole action
    # cfn_nag F40 IAM managed policy should not allow a * resource with
    #             PassRole action
    return await in_process(
        terraform_open_passrole,
        content=content,
        path=path,
        model=model,
    )


@CACHE_ETERNALLY
@SHIELD
@TIMEOUT_1MIN
async def run_terraform_permissive_policy(
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
    return await in_process(
        terraform_permissive_policy,
        content=content,
        path=path,
        model=model,
    )


@SHIELD
async def analyze(
    content_generator: Callable[[], str],
    file_extension: str,
    path: str,
    **_: None,
) -> List[Awaitable[Vulnerabilities]]:
    coroutines: List[Awaitable[Vulnerabilities]] = []

    if file_extension in EXTENSIONS_CLOUDFORMATION:
        content = content_generator()
        async for template in load_templates(content, fmt=file_extension):
            coroutines.append(
                run_cfn_admin_policy_attached(content, path, template)
            )
            coroutines.append(
                run_cfn_bucket_policy_allows_public_access(
                    content, path, template
                )
            )
            coroutines.append(
                run_cfn_iam_user_missing_role_based_security(
                    content, path, template
                )
            )
            coroutines.append(
                run_cfn_negative_statement(content, path, template)
            )
            coroutines.append(run_cfn_open_passrole(content, path, template))
            coroutines.append(
                run_cfn_permissive_policy(content, path, template)
            )

    elif file_extension in EXTENSIONS_TERRAFORM:
        content = content_generator()
        model = await load_terraform(stream=content, default=[])

        coroutines.append(
            run_terraform_admin_policy_attached(content, path, model)
        )
        coroutines.append(
            run_terraform_negative_statement(content, path, model)
        )
        coroutines.append(run_terraform_open_passrole(content, path, model))
        coroutines.append(
            run_terraform_permissive_policy(content, path, model)
        )

    return coroutines
