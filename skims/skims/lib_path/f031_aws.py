from aioextensions import (
    in_process,
)
from aws.iam.structure import (
    is_action_permissive,
    is_resource_permissive,
)
from aws.iam.utils import (
    match_pattern,
)
from aws.model import (
    AWSIamManagedPolicyArns,
    AWSIamPolicyStatement,
    AWSS3BucketPolicy,
)
from lib_path.common import (
    EXTENSIONS_CLOUDFORMATION,
    EXTENSIONS_TERRAFORM,
    get_aws_iterator,
    get_vulnerabilities_from_iterator_blocking,
    SHIELD,
)
from metaloaders.model import (
    Node,
)
from model import (
    core_model,
)
from parse_cfn.loader import (
    load_templates,
)
from parse_cfn.structure import (
    iter_s3_bucket_policies,
    iterate_iam_policy_documents as cfn_iterate_iam_policy_documents,
    iterate_managed_policy_arns as cnf_iterate_managed_policy_arns,
)
from parse_hcl2.loader import (
    load as load_terraform,
)
from parse_hcl2.structure.aws import (
    iterate_iam_policy_documents as terraform_iterate_iam_policy_documents,
    iterate_managed_policy_arns as terraform_iterate_managed_policy_arns,
)
from state.cache import (
    CACHE_ETERNALLY,
)
from typing import (
    Any,
    Awaitable,
    Callable,
    Iterator,
    List,
    Union,
)
from utils.function import (
    get_node_by_keys,
    TIMEOUT_1MIN,
)

_FINDING_F031 = core_model.FindingEnum.F031
_FINDING_F031_CWE = _FINDING_F031.value.cwe


def _is_iam_passrole(action: str) -> bool:
    return match_pattern(action, "iam:PassRole")


def _negative_statement_iterate_vulnerabilities(
    statements_iterator: Iterator[Union[AWSIamPolicyStatement, Node]]
) -> Iterator[Union[AWSIamPolicyStatement, Node]]:
    for stmt in statements_iterator:
        stmt_raw = stmt.raw if isinstance(stmt, Node) else stmt.data

        if stmt_raw["Effect"] != "Allow":
            continue

        if isinstance(stmt, Node):
            if "NotAction" in stmt_raw:
                yield from (
                    action
                    for action in stmt.inner.get("NotAction").data
                    if not is_action_permissive(action.raw)
                )

            if "NotResource" in stmt_raw:
                yield from (
                    resource
                    for resource in stmt.inner.get("NotResource").data
                    if not is_resource_permissive(resource.raw)
                )
        else:
            if "NotAction" in stmt_raw and not any(
                map(is_action_permissive, stmt_raw["NotAction"])
            ):
                yield stmt

            if "NotResource" in stmt_raw and not any(
                map(is_resource_permissive, stmt_raw["NotResource"])
            ):
                yield stmt


def _permissive_policy_iterate_vulnerabilities(
    statements_iterator: Iterator[Union[AWSIamPolicyStatement, Node]]
) -> Iterator[Union[AWSIamPolicyStatement, Node]]:
    for stmt in statements_iterator:
        stmt_raw = stmt.raw if isinstance(stmt, Node) else stmt.data
        if not (
            stmt_raw["Effect"] == "Allow"
            and "Principal" not in stmt_raw
            and "Condition" not in stmt_raw
        ):
            continue

        actions = stmt_raw.get("Action", [])
        resources = stmt_raw.get("Resource", [])
        has_permissive_resources = any(map(is_resource_permissive, resources))
        has_permissive_actions = any(map(is_action_permissive, actions))
        if (
            isinstance(stmt, Node)
            and has_permissive_resources
            and has_permissive_actions
        ):
            yield from (
                resource
                for resource in stmt.inner.get("Resource").data
                if is_resource_permissive(resource.raw)
            )
            yield from (
                action
                for action in stmt.inner.get("Action").data
                if is_action_permissive(action.raw)
            )

        elif has_permissive_resources and has_permissive_actions:
            yield stmt


def _open_passrole_iterate_vulnerabilities(
    statements_iterator: Iterator[Union[AWSIamPolicyStatement, Node]],
) -> Iterator[Union[AWSIamPolicyStatement, Node]]:
    for stmt in statements_iterator:
        stmt_raw = stmt.raw if isinstance(stmt, Node) else stmt.data
        if stmt_raw["Effect"] == "Allow":
            actions = stmt_raw.get("Action", [])
            resources = stmt_raw.get("Resource", [])
            if isinstance(stmt, Node) and actions and resources:
                actions = stmt.inner.get("Action")
                resources = stmt.inner.get("Resource")
                has_permissive_resources = any(
                    map(is_resource_permissive, resources.raw)
                )
                is_iam_passrole = any(map(_is_iam_passrole, actions.raw))

                if has_permissive_resources and is_iam_passrole:
                    yield from (
                        resource
                        for resource in resources.data
                        if is_resource_permissive(resource.raw)
                    )
                    yield from (
                        action
                        for action in actions.data
                        if _is_iam_passrole(action.raw)
                    )
            else:
                if all(
                    (
                        any(map(_is_iam_passrole, actions)),
                        any(map(is_resource_permissive, resources)),
                    )
                ):
                    yield stmt


def _admin_policies_attached_iterate_vulnerabilities(
    managed_policies_iterator: Iterator[Union[Node, AWSIamManagedPolicyArns]],
) -> Iterator[Union[Node, AWSIamManagedPolicyArns]]:
    elevated_policies = {
        "arn:aws:iam::aws:policy/PowerUserAccess",
        "arn:aws:iam::aws:policy/IAMFullAccess",
        "arn:aws:iam::aws:policy/AdministratorAccess",
    }
    for policies in managed_policies_iterator:
        if isinstance(policies, Node):
            yield from (
                policy
                for policy in policies.data
                if policy.raw in elevated_policies
            )
        elif any(
            policy in elevated_policies for policy in policies.data or []
        ):
            yield policies


def is_s3_action_writeable(actions: Union[AWSS3BucketPolicy, Node]) -> bool:
    action_start_with = [
        "Copy",
        "Create",
        "Delete",
        "Put",
        "Restore",
        "Update",
        "Upload",
        "Write",
    ]
    for action in actions.data:
        if any(
            action.raw.startswith(f"s3:{atw}") for atw in action_start_with
        ):
            return True
    return False


def _cfn_bucket_policy_allows_public_access_iterate_vulnerabilities(
    policies_iterator: Iterator[Union[AWSS3BucketPolicy, Node]],
) -> Iterator[Union[AWSS3BucketPolicy, Node]]:
    for policy in policies_iterator:
        statements = get_node_by_keys(policy, ["PolicyDocument", "Statement"])
        for statement in statements.data:
            effect = statement.raw.get("Effect", "")
            principal = statement.raw.get("Principal", "")
            if (
                effect == "Allow"
                and principal == "*"
                and is_s3_action_writeable(statement.inner["Action"])
            ):
                yield statement.inner["Principal"]


def _cfn_negative_statement(
    content: str,
    path: str,
    template: Any,
) -> core_model.Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        cwe={_FINDING_F031_CWE},
        description_key="src.lib_path.f031_aws.negative_statement",
        finding=_FINDING_F031,
        iterator=get_aws_iterator(
            _negative_statement_iterate_vulnerabilities(
                statements_iterator=cfn_iterate_iam_policy_documents(
                    template=template,
                )
            )
        ),
        path=path,
    )


@CACHE_ETERNALLY
@SHIELD
@TIMEOUT_1MIN
async def cfn_negative_statement(
    content: str,
    path: str,
    template: Any,
) -> core_model.Vulnerabilities:
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
) -> core_model.Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        cwe={_FINDING_F031_CWE},
        description_key="src.lib_path.f031_aws.permissive_policy",
        finding=_FINDING_F031,
        iterator=get_aws_iterator(
            _permissive_policy_iterate_vulnerabilities(
                statements_iterator=cfn_iterate_iam_policy_documents(
                    template=template,
                )
            )
        ),
        path=path,
    )


@CACHE_ETERNALLY
@SHIELD
@TIMEOUT_1MIN
async def cfn_permissive_policy(
    content: str,
    path: str,
    template: Any,
) -> core_model.Vulnerabilities:
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
) -> core_model.Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        cwe={_FINDING_F031_CWE},
        description_key="src.lib_path.f031_aws.open_passrole",
        finding=_FINDING_F031,
        iterator=get_aws_iterator(
            _open_passrole_iterate_vulnerabilities(
                statements_iterator=cfn_iterate_iam_policy_documents(
                    template=template,
                )
            )
        ),
        path=path,
    )


def _cfn_admin_policy_attached(
    content: str,
    path: str,
    template: Any,
) -> core_model.Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        cwe={_FINDING_F031_CWE},
        description_key="src.lib_path.f031_aws.permissive_policy",
        finding=_FINDING_F031,
        iterator=get_aws_iterator(
            _admin_policies_attached_iterate_vulnerabilities(
                managed_policies_iterator=cnf_iterate_managed_policy_arns(
                    template=template,
                ),
            )
        ),
        path=path,
    )


@CACHE_ETERNALLY
@SHIELD
@TIMEOUT_1MIN
async def cfn_open_passrole(
    content: str,
    path: str,
    template: Any,
) -> core_model.Vulnerabilities:
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
) -> core_model.Vulnerabilities:
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
) -> core_model.Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        cwe={_FINDING_F031_CWE},
        description_key="src.lib_path.f031_aws.negative_statement",
        finding=_FINDING_F031,
        iterator=get_aws_iterator(
            _negative_statement_iterate_vulnerabilities(
                statements_iterator=terraform_iterate_iam_policy_documents(
                    model=model,
                )
            )
        ),
        path=path,
    )


@CACHE_ETERNALLY
@SHIELD
@TIMEOUT_1MIN
async def terraform_negative_statement(
    content: str,
    path: str,
    model: Any,
) -> core_model.Vulnerabilities:
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
) -> core_model.Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        cwe={_FINDING_F031_CWE},
        description_key="src.lib_path.f031_aws.open_passrole",
        finding=_FINDING_F031,
        iterator=get_aws_iterator(
            _open_passrole_iterate_vulnerabilities(
                statements_iterator=terraform_iterate_iam_policy_documents(
                    model=model,
                )
            )
        ),
        path=path,
    )


@CACHE_ETERNALLY
@SHIELD
@TIMEOUT_1MIN
async def terraform_open_passrole(
    content: str,
    path: str,
    model: Any,
) -> core_model.Vulnerabilities:
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
) -> core_model.Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        cwe={_FINDING_F031_CWE},
        description_key="src.lib_path.f031_aws.permissive_policy",
        finding=_FINDING_F031,
        iterator=get_aws_iterator(
            _permissive_policy_iterate_vulnerabilities(
                statements_iterator=terraform_iterate_iam_policy_documents(
                    model=model,
                )
            )
        ),
        path=path,
    )


@CACHE_ETERNALLY
@SHIELD
@TIMEOUT_1MIN
async def terraform_permissive_policy(
    content: str,
    path: str,
    model: Any,
) -> core_model.Vulnerabilities:
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
) -> core_model.Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        cwe={_FINDING_F031_CWE},
        description_key="src.lib_path.f031_aws.permissive_policy",
        finding=_FINDING_F031,
        iterator=get_aws_iterator(
            _admin_policies_attached_iterate_vulnerabilities(
                managed_policies_iterator=(
                    terraform_iterate_managed_policy_arns(model=model)
                )
            )
        ),
        path=path,
    )


def _cfn_bucket_policy_allows_public_access(
    content: str,
    path: str,
    template: Any,
) -> core_model.Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        cwe={_FINDING_F031_CWE},
        description_key="src.lib_path.f031.bucket_policy_allows_public_access",
        finding=_FINDING_F031,
        iterator=get_aws_iterator(
            _cfn_bucket_policy_allows_public_access_iterate_vulnerabilities(
                policies_iterator=iter_s3_bucket_policies(template=template),
            )
        ),
        path=path,
    )


@CACHE_ETERNALLY
@SHIELD
@TIMEOUT_1MIN
async def terraform_admin_policy_attached(
    content: str,
    path: str,
    model: Any,
) -> core_model.Vulnerabilities:
    # cfn_nag W43 IAM role should not have AdministratorAccess policy
    return await in_process(
        _terraform_admin_policy_attached,
        content=content,
        path=path,
        model=model,
    )


@CACHE_ETERNALLY
@SHIELD
@TIMEOUT_1MIN
async def cfn_bucket_policy_allows_public_access(
    content: str,
    path: str,
    template: Any,
) -> core_model.Vulnerabilities:
    return await in_process(
        _cfn_bucket_policy_allows_public_access,
        content=content,
        path=path,
        template=template,
    )


@SHIELD
async def analyze(
    content_generator: Callable[[], Awaitable[str]],
    file_extension: str,
    path: str,
    **_: None,
) -> List[Awaitable[core_model.Vulnerabilities]]:
    coroutines: List[Awaitable[core_model.Vulnerabilities]] = []

    if file_extension in EXTENSIONS_CLOUDFORMATION:
        content = await content_generator()
        async for template in load_templates(
            content=content, fmt=file_extension
        ):
            coroutines.append(
                cfn_negative_statement(
                    content=content,
                    path=path,
                    template=template,
                )
            )
            coroutines.append(
                cfn_open_passrole(
                    content=content,
                    path=path,
                    template=template,
                )
            )
            coroutines.append(
                cfn_permissive_policy(
                    content=content,
                    path=path,
                    template=template,
                )
            )
            coroutines.append(
                cfn_admin_policy_attached(
                    content=content,
                    path=path,
                    template=template,
                )
            )
            coroutines.append(
                cfn_bucket_policy_allows_public_access(
                    content=content,
                    path=path,
                    template=template,
                )
            )
    elif file_extension in EXTENSIONS_TERRAFORM:
        content = await content_generator()
        model = await load_terraform(stream=content, default=[])
        coroutines.append(
            terraform_negative_statement(
                content=content,
                path=path,
                model=model,
            )
        )
        coroutines.append(
            terraform_open_passrole(
                content=content,
                path=path,
                model=model,
            )
        )
        coroutines.append(
            terraform_permissive_policy(
                content=content,
                path=path,
                model=model,
            )
        )
        coroutines.append(
            terraform_admin_policy_attached(
                content=content,
                path=path,
                model=model,
            )
        )

    return coroutines
