# Standard library
from typing import (
    Any,
    Awaitable,
    Callable,
    Iterator,
    List,
    Union,
)

# Third party libraries
from aioextensions import (
    in_process,
)
from metaloaders.model import (
    Node,
)

# Local libraries
from aws.iam.structure import (
    is_action_permissive,
    is_resource_permissive,
)
from aws.model import (
    AWSIamManagedPolicyArns,
    AWSIamPolicyStatement,
)
from aws.iam.utils import (
    match_pattern,
)
from lib_path.common import (
    get_vulnerabilities_from_aws_iterator_blocking,
    EXTENSIONS_CLOUDFORMATION,
    EXTENSIONS_TERRAFORM,
    SHIELD,
)
from parse_cfn.structure import (
    iterate_iam_policy_documents as cfn_iterate_iam_policy_documents,
    iterate_managed_policy_arns as cnf_iterate_managed_policy_arns,
)
from parse_cfn.loader import (
    load_templates,
)
from parse_hcl2.loader import (
    load as load_terraform,
)
from parse_hcl2.structure import (
    iterate_iam_policy_documents as terraform_iterate_iam_policy_documents,
    iterate_managed_policy_arns as terraform_iterate_managed_policy_arns,
)
from state.cache import (
    CACHE_ETERNALLY,
)
from utils.function import (
    TIMEOUT_1MIN,
)
from model.core_model import (
    FindingEnum,
    Vulnerabilities,
)


def _is_iam_passrole(action: str) -> bool:
    return match_pattern(action, 'iam:PassRole')


def _negative_statement_iterate_vulnerabilities(
    statements_iterator: Iterator[Union[AWSIamPolicyStatement, Node]]
) -> Iterator[Union[AWSIamPolicyStatement, Node]]:
    for stmt in statements_iterator:
        stmt_raw = stmt.raw if isinstance(stmt, Node) else stmt.data

        if stmt_raw['Effect'] != 'Allow':
            continue

        if isinstance(stmt, Node):
            if 'NotAction' in stmt_raw:
                yield from (action
                            for action in stmt.inner.get('NotAction').data
                            if not is_action_permissive(action.raw))

            if 'NotResource' in stmt_raw:
                yield from (resource
                            for resource in stmt.inner.get('NotResource').data
                            if not is_resource_permissive(resource.raw))
        else:
            if 'NotAction' in stmt_raw:
                if not any(map(is_action_permissive, stmt_raw['NotAction'])):
                    yield stmt

            if 'NotResource' in stmt_raw:
                if not any(map(is_resource_permissive,
                               stmt_raw['NotResource'])):
                    yield stmt


def _permissive_policy_iterate_vulnerabilities(
    statements_iterator: Iterator[Union[AWSIamPolicyStatement, Node]]
) -> Iterator[Union[AWSIamPolicyStatement, Node]]:
    for stmt in statements_iterator:
        stmt_raw = stmt.raw if isinstance(stmt, Node) else stmt.data
        if not (stmt_raw['Effect'] == 'Allow' and 'Principal' not in stmt_raw
                and 'Condition' not in stmt_raw):
            continue

        actions = stmt_raw.get('Action', [])
        resources = stmt_raw.get('Resource', [])
        has_permissive_resources = any(map(is_resource_permissive, resources))
        has_permissive_actions = any(map(is_action_permissive, actions))
        if (isinstance(stmt, Node) and has_permissive_resources
                and has_permissive_actions):
            yield from (resource
                        for resource in stmt.inner.get('Resource').data
                        if is_resource_permissive(resource.raw))
            yield from (action for action in stmt.inner.get('Action').data
                        if is_action_permissive(action.raw))

        elif has_permissive_resources and has_permissive_actions:
            yield stmt


def _open_passrole_iterate_vulnerabilities(
    statements_iterator: Iterator[Union[AWSIamPolicyStatement, Node]],
) -> Iterator[Union[AWSIamPolicyStatement, Node]]:
    for stmt in statements_iterator:
        stmt_raw = stmt.raw if isinstance(stmt, Node) else stmt.data
        if stmt_raw['Effect'] == 'Allow':
            actions = stmt_raw.get('Action', [])
            resources = stmt_raw.get('Resource', [])
            if isinstance(stmt, Node) and actions and resources:
                actions = stmt.inner.get('Action')
                resources = stmt.inner.get('Resource')
                has_permissive_resources = any(
                    map(is_resource_permissive, resources.raw))
                is_iam_passrole = any(map(_is_iam_passrole, actions.raw))

                if has_permissive_resources and is_iam_passrole:
                    yield from (resource for resource in resources.data
                                if is_resource_permissive(resource.raw))
                    yield from (action for action in actions.data
                                if _is_iam_passrole(action.raw))
            else:
                if all((
                    any(map(_is_iam_passrole, actions)),
                    any(map(is_resource_permissive, resources)),
                )):
                    yield stmt


def _admin_policies_attached_iterate_vulnerabilities(
    managed_policies_iterator: Iterator[Union[Node, AWSIamManagedPolicyArns]],
) -> Iterator[Union[Node, AWSIamManagedPolicyArns]]:
    elevated_policies = {
        'arn:aws:iam::aws:policy/PowerUserAccess',
        'arn:aws:iam::aws:policy/IAMFullAccess',
        'arn:aws:iam::aws:policy/AdministratorAccess',
    }
    for policies in managed_policies_iterator:
        if isinstance(policies, Node):
            yield from (policy for policy in policies.data
                        if policy.raw in elevated_policies)
        elif any(policy in elevated_policies
                 for policy in policies.data or list()):
            yield policies


def _cfn_negative_statement(
    content: str,
    path: str,
    template: Any,
) -> Vulnerabilities:
    return get_vulnerabilities_from_aws_iterator_blocking(
        content=content,
        description_key='src.lib_path.f031_aws.negative_statement',
        finding=FindingEnum.F031_AWS,
        path=path,
        statements_iterator=_negative_statement_iterate_vulnerabilities(
            statements_iterator=cfn_iterate_iam_policy_documents(
                template=template,
            )
        )
    )


@CACHE_ETERNALLY
@SHIELD
@TIMEOUT_1MIN
async def cfn_negative_statement(
    content: str,
    path: str,
    template: Any,
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
        _cfn_negative_statement,
        content=content,
        path=path,
        template=template,
    )


def _cfn_permissive_policy(
    content: str,
    path: str,
    template: Any,
) -> Vulnerabilities:
    return get_vulnerabilities_from_aws_iterator_blocking(
        content=content,
        description_key='src.lib_path.f031_aws.permissive_policy',
        finding=FindingEnum.F031_AWS,
        path=path,
        statements_iterator=_permissive_policy_iterate_vulnerabilities(
            statements_iterator=cfn_iterate_iam_policy_documents(
                template=template,
            )
        )
    )


@CACHE_ETERNALLY
@SHIELD
@TIMEOUT_1MIN
async def cfn_permissive_policy(
    content: str,
    path: str,
    template: Any,
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
        _cfn_permissive_policy,
        content=content,
        path=path,
        template=template,
    )


def _cfn_open_passrole(
    content: str,
    path: str,
    template: Any,
) -> Vulnerabilities:
    return get_vulnerabilities_from_aws_iterator_blocking(
        content=content,
        description_key='src.lib_path.f031_aws.open_passrole',
        finding=FindingEnum.F031_AWS,
        path=path,
        statements_iterator=_open_passrole_iterate_vulnerabilities(
            statements_iterator=cfn_iterate_iam_policy_documents(
                template=template,
            )
        )
    )


def _cfn_admin_policy_attached(
    content: str,
    path: str,
    template: Any,
) -> Vulnerabilities:
    return get_vulnerabilities_from_aws_iterator_blocking(
        content=content,
        description_key='src.lib_path.f031_aws.permissive_policy',
        finding=FindingEnum.F031_AWS,
        path=path,
        statements_iterator=_admin_policies_attached_iterate_vulnerabilities(
            managed_policies_iterator=cnf_iterate_managed_policy_arns(
                template=template,
            ),
        ),
    )


@CACHE_ETERNALLY
@SHIELD
@TIMEOUT_1MIN
async def cfn_open_passrole(
    content: str,
    path: str,
    template: Any,
) -> Vulnerabilities:
    # cfn_nag F38 IAM role should not allow * resource with PassRole action
    #             on its permissions policy
    # cfn_nag F39 IAM policy should not allow * resource with PassRole action
    # cfn_nag F40 IAM managed policy should not allow a * resource with
    #             PassRole action
    return await in_process(
        _cfn_open_passrole,
        content=content,
        path=path,
        template=template,
    )


@CACHE_ETERNALLY
@SHIELD
@TIMEOUT_1MIN
async def cfn_admin_policy_attached(
    content: str,
    path: str,
    template: Any,
) -> Vulnerabilities:
    # cfn_nag W43 IAM role should not have AdministratorAccess policy
    return await in_process(
        _cfn_admin_policy_attached,
        content=content,
        path=path,
        template=template,
    )


def _terraform_negative_statement(
    content: str,
    path: str,
    model: Any,
) -> Vulnerabilities:
    return get_vulnerabilities_from_aws_iterator_blocking(
        content=content,
        description_key='src.lib_path.f031_aws.negative_statement',
        finding=FindingEnum.F031_AWS,
        path=path,
        statements_iterator=_negative_statement_iterate_vulnerabilities(
            statements_iterator=terraform_iterate_iam_policy_documents(
                model=model,
            )
        )
    )


@CACHE_ETERNALLY
@SHIELD
@TIMEOUT_1MIN
async def terraform_negative_statement(
    content: str,
    path: str,
    model: Any,
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
        _terraform_negative_statement,
        content=content,
        path=path,
        model=model,
    )


def _terraform_open_passrole(
    content: str,
    path: str,
    model: Any,
) -> Vulnerabilities:
    return get_vulnerabilities_from_aws_iterator_blocking(
        content=content,
        description_key='src.lib_path.f031_aws.open_passrole',
        finding=FindingEnum.F031_AWS,
        path=path,
        statements_iterator=_open_passrole_iterate_vulnerabilities(
            statements_iterator=terraform_iterate_iam_policy_documents(
                model=model,
            )
        )
    )


@CACHE_ETERNALLY
@SHIELD
@TIMEOUT_1MIN
async def terraform_open_passrole(
    content: str,
    path: str,
    model: Any,
) -> Vulnerabilities:
    # cfn_nag F38 IAM role should not allow * resource with PassRole action
    #             on its permissions policy
    # cfn_nag F39 IAM policy should not allow * resource with PassRole action
    # cfn_nag F40 IAM managed policy should not allow a * resource with
    #             PassRole action
    return await in_process(
        _terraform_open_passrole,
        content=content,
        path=path,
        model=model,
    )


def _terraform_permissive_policy(
    content: str,
    path: str,
    model: Any,
) -> Vulnerabilities:
    return get_vulnerabilities_from_aws_iterator_blocking(
        content=content,
        description_key='src.lib_path.f031_aws.permissive_policy',
        finding=FindingEnum.F031_AWS,
        path=path,
        statements_iterator=_permissive_policy_iterate_vulnerabilities(
            statements_iterator=terraform_iterate_iam_policy_documents(
                model=model,
            )
        )
    )


@CACHE_ETERNALLY
@SHIELD
@TIMEOUT_1MIN
async def terraform_permissive_policy(
    content: str,
    path: str,
    model: Any,
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
        _terraform_permissive_policy,
        content=content,
        path=path,
        model=model,
    )


def _terraform_admin_policy_attached(
    content: str,
    path: str,
    model: Any,
) -> Vulnerabilities:
    return get_vulnerabilities_from_aws_iterator_blocking(
        content=content,
        description_key='src.lib_path.f031_aws.permissive_policy',
        finding=FindingEnum.F031_AWS,
        path=path,
        statements_iterator=_admin_policies_attached_iterate_vulnerabilities(
            managed_policies_iterator=terraform_iterate_managed_policy_arns(
                model=model,
            ),
        ),
    )


@CACHE_ETERNALLY
@SHIELD
@TIMEOUT_1MIN
async def terraform_admin_policy_attached(
    content: str,
    path: str,
    model: Any,
) -> Vulnerabilities:
    # cfn_nag W43 IAM role should not have AdministratorAccess policy
    return await in_process(
        _terraform_admin_policy_attached,
        content=content,
        path=path,
        model=model,
    )


@SHIELD
async def analyze(
    content_generator: Callable[[], Awaitable[str]],
    file_extension: str,
    path: str,
    **_: None,
) -> List[Awaitable[Vulnerabilities]]:
    coroutines: List[Awaitable[Vulnerabilities]] = []

    if file_extension in EXTENSIONS_CLOUDFORMATION:
        content = await content_generator()
        async for template in load_templates(content=content,
                                             fmt=file_extension):
            coroutines.append(cfn_negative_statement(
                content=content,
                path=path,
                template=template,
            ))
            coroutines.append(cfn_open_passrole(
                content=content,
                path=path,
                template=template,
            ))
            coroutines.append(cfn_permissive_policy(
                content=content,
                path=path,
                template=template,
            ))
            coroutines.append(cfn_admin_policy_attached(
                content=content,
                path=path,
                template=template,
            ))
    elif file_extension in EXTENSIONS_TERRAFORM:
        content = await content_generator()
        model = await load_terraform(stream=content, default=[])
        coroutines.append(terraform_negative_statement(
            content=content,
            path=path,
            model=model,
        ))
        coroutines.append(terraform_open_passrole(
            content=content,
            path=path,
            model=model,
        ))
        coroutines.append(terraform_permissive_policy(
            content=content,
            path=path,
            model=model,
        ))
        coroutines.append(terraform_admin_policy_attached(
            content=content,
            path=path,
            model=model,
        ))

    return coroutines
