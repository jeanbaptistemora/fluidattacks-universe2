from aioextensions import (
    in_process,
)
from aws.model import (
    AWSIamManagedPolicy,
    AWSKmsKey,
)
from aws.services import (
    ACTIONS,
)
from lib_path.common import (
    EXTENSIONS_CLOUDFORMATION,
    get_cloud_iterator,
    get_line_by_extension,
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
    iter_iam_managed_policies_and_mgd_policies,
    iter_iam_managed_policies_and_roles,
    iter_kms_keys,
)
import re
from state.cache import (
    CACHE_ETERNALLY,
)
from typing import (
    Any,
    Awaitable,
    Callable,
    Iterator,
    List,
    Optional,
    Pattern,
    Union,
)
from utils.function import (
    get_node_by_keys,
    TIMEOUT_1MIN,
)

_FINDING_F325 = core_model.FindingEnum.F325
_FINDING_F325_CWE = _FINDING_F325.value.cwe


def _cfn_kms_key_has_master_keys_exposed_to_everyone_iter_vulns(
    keys_iterator: Iterator[Union[AWSKmsKey, Node]],
) -> Iterator[Union[AWSKmsKey, Node]]:
    for key in keys_iterator:
        statements = get_node_by_keys(key, ["KeyPolicy", "Statement"])
        for stmt in statements.data:
            effect = stmt.raw.get("Effect")
            principal = get_node_by_keys(stmt, ["Principal", "AWS"])
            if (
                isinstance(principal, Node)
                and effect == "Allow"
                and principal.raw == "*"
            ):
                yield principal


def resource_all_(resource_node: Node) -> Optional[Node]:
    """Check if an action is permitted for any resource."""
    resources = (
        resource_node.data
        if isinstance(resource_node.data, list)
        else [resource_node]
    )
    for res in resources:
        if res.raw == "*":
            return res
    return None


def policy_actions_has_privilege(action_node: Node, privilege: str) -> bool:
    """Check if an action have a privilege."""
    write_actions: dict = ACTIONS
    actions = (
        action_node.data
        if isinstance(action_node.data, list)
        else [action_node]
    )
    for act in actions:
        if act.raw == "*":
            return True
        serv, act_val = act.raw.split(":")
        if act_val.startswith("*"):
            return True
        act_val = (
            act_val[: act_val.index("*")] if act_val.endswith("*") else act_val
        )
        if act_val in write_actions.get(serv, {}).get(privilege, []):
            return True
    return False


def policy_statement_privilege(statements: Node) -> Iterator[Node]:
    """Check if a statement of a policy allow an action in all resources."""
    for stm in statements.data:
        effect = get_node_by_keys(stm, ["Effect"])
        resource = get_node_by_keys(stm, ["Resource"])
        action = get_node_by_keys(stm, ["Action"])
        wild_res_node = resource_all_(resource) if resource else None
        if (
            effect.raw == "Allow"
            and wild_res_node
            and action
            and policy_actions_has_privilege(action, "write")
        ):
            yield wild_res_node


def _cfn_iam_has_wildcard_resource_on_write_action_iter_vulns(
    iam_iterator: Iterator[Union[AWSIamManagedPolicy, Node]],
) -> Iterator[Union[AWSIamManagedPolicy, Node]]:
    for iam_res in iam_iterator:
        policies = (
            iam_res.inner["Policies"].data
            if "Policies" in iam_res.raw
            else [iam_res]
        )
        for policy in policies:
            statements = get_node_by_keys(
                policy, ["PolicyDocument", "Statement"]
            )
            if isinstance(statements, Node):
                yield from policy_statement_privilege(statements)


def get_wildcard_nodes(act_res: Node, pattern: Pattern) -> Iterator[Node]:
    for act in act_res.data if isinstance(act_res.raw, List) else [act_res]:
        if pattern.match(act.raw):
            yield act


def is_statement_miss_configured(file_ext: str, stmt: Node) -> Iterator[Node]:
    wildcard_action: Pattern = re.compile(r"^(\*)|(\w+:\*)$")
    wildcard_resource: Pattern = re.compile(r"^(\*)$")
    effect = stmt.inner.get("Effect")
    if effect.raw == "Allow":
        if no_action := stmt.inner.get("NotAction"):
            yield AWSIamManagedPolicy(
                column=no_action.start_column,
                data=no_action.data,
                line=get_line_by_extension(no_action.start_line, file_ext),
            ) if isinstance(no_action.raw, List) else no_action
        if no_resource := stmt.inner.get("NotResource"):
            yield AWSIamManagedPolicy(
                column=no_resource.start_column,
                data=no_resource.data,
                line=get_line_by_extension(no_resource.start_line, file_ext),
            ) if isinstance(no_resource.raw, List) else no_resource
        action = stmt.inner.get("Action")
        if action:
            yield from get_wildcard_nodes(action, wildcard_action)
        resource = stmt.inner.get("Resource")
        if resource:
            yield from get_wildcard_nodes(resource, wildcard_resource)


def _cfn_iam_is_policy_miss_configured_iter_vulns(
    file_ext: str,
    iam_iterator: Iterator[Union[AWSIamManagedPolicy, Node]],
) -> Iterator[Union[AWSIamManagedPolicy, Node]]:
    for iam_res in iam_iterator:
        pol_document = iam_res.inner.get("PolicyDocument")
        statements = pol_document.inner.get("Statement")
        for stmt in statements.data:
            yield from is_statement_miss_configured(file_ext, stmt)
        if users := iam_res.inner.get("Users"):
            yield AWSIamManagedPolicy(
                column=users.start_column,
                data=users.data,
                line=get_line_by_extension(users.start_line, file_ext),
            )


def _cfn_kms_key_has_master_keys_exposed_to_everyone(
    content: str,
    path: str,
    template: Any,
) -> core_model.Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        cwe={_FINDING_F325_CWE},
        description_key=(
            "src.lib_path.f325.kms_key_has_master_keys_exposed_to_everyone"
        ),
        finding=_FINDING_F325,
        iterator=get_cloud_iterator(
            _cfn_kms_key_has_master_keys_exposed_to_everyone_iter_vulns(
                keys_iterator=iter_kms_keys(template=template),
            )
        ),
        path=path,
    )


def _cfn_iam_has_wildcard_resource_on_write_action(
    content: str,
    path: str,
    template: Any,
) -> core_model.Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        cwe={_FINDING_F325_CWE},
        description_key=(
            "src.lib_path.f325.iam_has_wildcard_resource_on_write_action"
        ),
        finding=_FINDING_F325,
        iterator=get_cloud_iterator(
            _cfn_iam_has_wildcard_resource_on_write_action_iter_vulns(
                iam_iterator=iter_iam_managed_policies_and_roles(
                    template=template
                ),
            )
        ),
        path=path,
    )


def _cfn_iam_is_policy_miss_configured(
    content: str,
    file_ext: str,
    path: str,
    template: Any,
) -> core_model.Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        cwe={_FINDING_F325_CWE},
        description_key=("src.lib_path.f325.iam_is_policy_miss_configured"),
        finding=_FINDING_F325,
        iterator=get_cloud_iterator(
            _cfn_iam_is_policy_miss_configured_iter_vulns(
                file_ext=file_ext,
                iam_iterator=iter_iam_managed_policies_and_mgd_policies(
                    template=template
                ),
            )
        ),
        path=path,
    )


@CACHE_ETERNALLY
@SHIELD
@TIMEOUT_1MIN
async def cfn_kms_key_has_master_keys_exposed_to_everyone(
    content: str,
    path: str,
    template: Any,
) -> core_model.Vulnerabilities:
    return await in_process(
        _cfn_kms_key_has_master_keys_exposed_to_everyone,
        content=content,
        path=path,
        template=template,
    )


@CACHE_ETERNALLY
@SHIELD
@TIMEOUT_1MIN
async def cfn_iam_has_wildcard_resource_on_write_action(
    content: str,
    path: str,
    template: Any,
) -> core_model.Vulnerabilities:
    return await in_process(
        _cfn_iam_has_wildcard_resource_on_write_action,
        content=content,
        path=path,
        template=template,
    )


@CACHE_ETERNALLY
@SHIELD
@TIMEOUT_1MIN
async def cfn_iam_is_policy_miss_configured(
    content: str,
    file_ext: str,
    path: str,
    template: Any,
) -> core_model.Vulnerabilities:
    return await in_process(
        _cfn_iam_is_policy_miss_configured,
        content=content,
        file_ext=file_ext,
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
                cfn_kms_key_has_master_keys_exposed_to_everyone(
                    content=content,
                    path=path,
                    template=template,
                )
            )
            coroutines.append(
                cfn_iam_has_wildcard_resource_on_write_action(
                    content=content,
                    path=path,
                    template=template,
                )
            )
            coroutines.append(
                cfn_iam_is_policy_miss_configured(
                    content=content,
                    file_ext=file_extension,
                    path=path,
                    template=template,
                )
            )

    return coroutines
