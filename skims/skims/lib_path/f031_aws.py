# Standard library
from typing import (
    Any,
    Awaitable,
    Callable,
    Iterator,
    List,
    Tuple,
    Union,
)

# Third party libraries
from aioextensions import (
    resolve,
    in_process,
)
from metaloaders.model import Node

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
    blocking_get_vulnerabilities_from_iterator,
    EXTENSIONS_CLOUDFORMATION,
    EXTENSIONS_TERRAFORM,
    SHIELD,
)
from parse_cfn.loader_new import (
    load as load_cfn,
)
from parse_cfn.structure_new import (
    iterate_iam_policy_documents as cfn_iterate_iam_policy_documents,
    iterate_managed_policy_arns as cnf_iterate_managed_policy_arns,
)
from parse_hcl2.loader import (
    load as load_terraform,
)
from parse_hcl2.structure import (
    iterate_iam_policy_documents as terraform_iterate_iam_policy_documents,
)
from state.cache import (
    cache_decorator,
)
from state.ephemeral import (
    EphemeralStore,
)
from utils.model import (
    FindingEnum,
    Vulnerability,
)
from zone import (
    t,
)


def _is_iam_passrole(action: str) -> bool:
    return match_pattern(action, 'iam:PassRole')


def _create_vulns(
    content: str,
    description_key: str,
    path: str,
    statements_iterator: Iterator[Union[
        AWSIamManagedPolicyArns,
        AWSIamPolicyStatement,
        Node,
    ]],
) -> Tuple[Vulnerability, ...]:
    return blocking_get_vulnerabilities_from_iterator(
        content=content,
        description=t(
            key=description_key,
            path=path,
        ),
        finding=FindingEnum.F031_AWS,
        iterator=((
            stmt.start_line if isinstance(stmt, Node) else stmt.line,
            stmt.start_column if isinstance(stmt, Node) else stmt.column,
        ) for stmt in statements_iterator),
        path=path,
    )


def _negative_statement_iterate_vulnerabilities(
    statements_iterator: Iterator[Union[AWSIamPolicyStatement, Node]]
) -> Iterator[Union[AWSIamPolicyStatement, Node]]:
    for stmt in statements_iterator:
        stmt_raw = stmt.raw if isinstance(stmt, Node) else stmt.data

        if stmt_raw['Effect'] != 'Allow':
            continue

        if 'NotAction' in stmt_raw:
            if not any(map(is_action_permissive, stmt_raw['NotAction'])):
                yield stmt

        if 'NotResource' in stmt_raw:
            if not any(map(is_resource_permissive, stmt_raw['NotResource'])):
                yield stmt


def _permissive_policy_iterate_vulnerabilities(
    statements_iterator: Iterator[Union[AWSIamPolicyStatement, Node]]
) -> Iterator[Union[AWSIamPolicyStatement, Node]]:
    for stmt in statements_iterator:
        stmt_raw = stmt.raw if isinstance(stmt, Node) else stmt.data

        actions = stmt_raw.get('Action', [])

        if (stmt_raw['Effect'] == 'Allow' and 'Principal' not in stmt_raw
                and 'Condition' not in stmt_raw):

            actions = stmt_raw.get('Action', [])
            resources = stmt_raw.get('Resource', [])
            if all((
                    any(map(is_action_permissive, actions)),
                    any(map(is_resource_permissive, resources)),
            )):
                yield stmt


def _open_passrole_iterate_vulnerabilities(
    statements_iterator: Iterator[Union[AWSIamPolicyStatement, Node]],
) -> Iterator[Union[AWSIamPolicyStatement, Node]]:
    for stmt in statements_iterator:
        stmt_raw = stmt.raw if isinstance(stmt, Node) else stmt.data
        if stmt_raw['Effect'] == 'Allow':
            actions = stmt_raw.get('Action', [])
            resources = stmt_raw.get('Resource', [])

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
) -> Tuple[Vulnerability, ...]:
    return _create_vulns(
        content=content,
        description_key='src.lib_path.f031_aws.negative_statement',
        path=path,
        statements_iterator=_negative_statement_iterate_vulnerabilities(
            statements_iterator=cfn_iterate_iam_policy_documents(
                template=template,
            )
        )
    )


@cache_decorator()
@SHIELD
async def cfn_negative_statement(
    content: str,
    path: str,
    template: Any,
) -> Tuple[Vulnerability, ...]:
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
) -> Tuple[Vulnerability, ...]:
    return _create_vulns(
        content=content,
        description_key='src.lib_path.f031_aws.permissive_policy',
        path=path,
        statements_iterator=_permissive_policy_iterate_vulnerabilities(
            statements_iterator=cfn_iterate_iam_policy_documents(
                template=template,
            )
        )
    )


@cache_decorator()
@SHIELD
async def cfn_permissive_policy(
    content: str,
    path: str,
    template: Any,
) -> Tuple[Vulnerability, ...]:
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
) -> Tuple[Vulnerability, ...]:
    return _create_vulns(
        content=content,
        description_key='src.lib_path.f031_aws.open_passrole',
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
) -> Tuple[Vulnerability, ...]:
    return _create_vulns(
        content=content,
        description_key='src.lib_path.f031_aws.permissive_policy',
        path=path,
        statements_iterator=_admin_policies_attached_iterate_vulnerabilities(
            managed_policies_iterator=cnf_iterate_managed_policy_arns(
                template=template,
            ),
        ),
    )


@cache_decorator()
@SHIELD
async def cfn_open_passrole(
    content: str,
    path: str,
    template: Any,
) -> Tuple[Vulnerability, ...]:
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


@cache_decorator()
@SHIELD
async def cfn_admin_policy_attached(
    content: str,
    path: str,
    template: Any,
) -> Tuple[Vulnerability, ...]:
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
) -> Tuple[Vulnerability, ...]:
    return _create_vulns(
        content=content,
        description_key='src.lib_path.f031_aws.negative_statement',
        path=path,
        statements_iterator=_negative_statement_iterate_vulnerabilities(
            statements_iterator=terraform_iterate_iam_policy_documents(
                model=model,
            )
        )
    )


@SHIELD
async def terraform_negative_statement(
    content: str,
    path: str,
    model: Any,
) -> Tuple[Vulnerability, ...]:
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
) -> Tuple[Vulnerability, ...]:
    return _create_vulns(
        content=content,
        description_key='src.lib_path.f031_aws.open_passrole',
        path=path,
        statements_iterator=_open_passrole_iterate_vulnerabilities(
            statements_iterator=terraform_iterate_iam_policy_documents(
                model=model,
            )
        )
    )


@SHIELD
async def terraform_open_passrole(
    content: str,
    path: str,
    model: Any,
) -> Tuple[Vulnerability, ...]:
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
) -> Tuple[Vulnerability, ...]:
    return _create_vulns(
        content=content,
        description_key='src.lib_path.f031_aws.permissive_policy',
        path=path,
        statements_iterator=_permissive_policy_iterate_vulnerabilities(
            statements_iterator=terraform_iterate_iam_policy_documents(
                model=model,
            )
        )
    )


@SHIELD
async def terraform_permissive_policy(
    content: str,
    path: str,
    model: Any,
) -> Tuple[Vulnerability, ...]:
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


async def analyze(
    content_generator: Callable[[], Awaitable[str]],
    file_extension: str,
    path: str,
    store: EphemeralStore,
) -> None:
    coroutines: List[Awaitable[Tuple[Vulnerability, ...]]] = []

    if file_extension in EXTENSIONS_CLOUDFORMATION:
        content = await content_generator()
        template = await load_cfn(content=content, fmt=file_extension)
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

    for results in resolve(coroutines, worker_greediness=1):
        for result in await results:
            await store.store(result)
