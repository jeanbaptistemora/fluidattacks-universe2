from aws.model import (
    AWSIamManagedPolicy,
    AWSKmsKey,
)
from aws.services import (
    ACTIONS,
)
from lib_path.common import (
    get_cloud_iterator,
    get_line_by_extension,
    get_vulnerabilities_from_iterator_blocking,
)
from metaloaders.model import (
    Node,
)
from model.core_model import (
    DeveloperEnum,
    FindingEnum,
    Vulnerabilities,
)
from parse_cfn.structure import (
    iter_iam_managed_policies_and_mgd_policies,
    iter_iam_managed_policies_and_roles,
    iter_iam_roles,
    iter_kms_keys,
)
import re
from typing import (
    Any,
    Iterator,
    List,
    Optional,
    Pattern,
    Union,
)
from utils.function import (
    get_node_by_keys,
)

WILDCARD_ACTION: Pattern = re.compile(r"^((\*)|(\w+:\*))$")
WILDCARD_RESOURCE: Pattern = re.compile(r"^(\*)$")


def get_wildcard_nodes(act_res: Node, pattern: Pattern) -> Iterator[Node]:
    for act in act_res.data if isinstance(act_res.raw, List) else [act_res]:
        if pattern.match(act.raw):
            yield act


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


def _policy_actions_has_privilege(action_node: Node, privilege: str) -> bool:
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


def _resource_all(resource_node: Node) -> Optional[Node]:
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


def _policy_statement_privilege(statements: Node) -> Iterator[Node]:
    """Check if a statement of a policy allow an action in all resources."""
    for stm in statements.data:
        effect = get_node_by_keys(stm, ["Effect"])
        resource = get_node_by_keys(stm, ["Resource"])
        action = get_node_by_keys(stm, ["Action"])
        wild_res_node = _resource_all(resource) if resource else None
        if (
            effect.raw == "Allow"
            and wild_res_node
            and action
            and _policy_actions_has_privilege(action, "write")
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
                yield from _policy_statement_privilege(statements)


def _service_is_present_action(
    action_node: Node, service: str
) -> Iterator[Node]:
    actions = (
        action_node.data
        if isinstance(action_node.data, list)
        else [action_node]
    )
    for act in actions:
        if act.raw == "*":
            yield act
        elif act.raw.split(":")[0] == service:
            yield act


def _iam_is_present_in_action(stmt: Node) -> Iterator[Node]:
    effect = stmt.inner.get("Effect")
    if effect.raw == "Allow" and (action := stmt.inner.get("Action")):
        yield from _service_is_present_action(action, "iam")


def _cfn_iam_has_privileges_over_iam_iter_vulns(
    iam_iterator: Iterator[Union[AWSIamManagedPolicy, Node]],
) -> Iterator[Union[AWSIamManagedPolicy, Node]]:
    for iam_res in iam_iterator:
        policies = (
            iam_res.inner["Policies"].data
            if "Policies" in iam_res.raw
            else [iam_res]
        )
        for policy in policies:
            if statements := get_node_by_keys(
                policy, ["PolicyDocument", "Statement"]
            ):
                for stmt in statements.data or []:
                    yield from _iam_is_present_in_action(stmt)


def _is_statement_miss_configured(file_ext: str, stmt: Node) -> Iterator[Node]:
    wildcard_action: Pattern = re.compile(r"^((\*)|(\w+:\*))$")
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
            yield from _is_statement_miss_configured(file_ext, stmt)
        if users := iam_res.inner.get("Users"):
            yield AWSIamManagedPolicy(
                column=users.start_column,
                data=users.data,
                line=get_line_by_extension(users.start_line, file_ext),
            )


def _check_assume_role_policies(
    assume_role_policy: Node, file_ext: str
) -> Iterator[Node]:
    statements = assume_role_policy.inner.get("Statement")
    for stmt in statements.data if statements else []:
        not_princ = stmt.inner.get("NotPrincipal")
        actions = stmt.inner.get("Action")
        effect = stmt.inner.get("Effect")

        if effect.raw != "Allow":
            continue

        if not_actions := stmt.inner.get("NotAction"):
            yield AWSIamManagedPolicy(
                column=not_actions.start_column,
                data=not_actions.data,
                line=get_line_by_extension(not_actions.start_line, file_ext),
            ) if isinstance(not_actions.raw, List) else not_actions

        if not_princ := stmt.inner.get("NotPrincipal"):
            yield AWSIamManagedPolicy(
                column=not_princ.start_column,
                data=not_princ.data,
                line=get_line_by_extension(not_princ.start_line, file_ext),
            )

        if actions:
            yield from get_wildcard_nodes(actions, WILDCARD_ACTION)


def _check_policy_documents(policies: Node, file_ext: str) -> Iterator[Node]:
    for policy in policies.data if policies else []:
        statements = get_node_by_keys(policy, ["PolicyDocument", "Statement"])
        for stmt in statements.data if statements else []:
            effect = stmt.inner.get("Effect")
            resources = stmt.inner.get("Resource")
            actions = stmt.inner.get("Action")

            if effect.raw != "Allow":
                continue

            if not_actions := stmt.inner.get("NotAction"):
                yield AWSIamManagedPolicy(
                    column=not_actions.start_column,
                    data=not_actions.data,
                    line=get_line_by_extension(
                        not_actions.start_line, file_ext
                    ),
                ) if isinstance(not_actions.raw, List) else not_actions

            if not_resource := stmt.inner.get("NotResource"):
                yield AWSIamManagedPolicy(
                    column=not_resource.start_column,
                    data=not_resource.data,
                    line=get_line_by_extension(
                        not_resource.start_line, file_ext
                    ),
                ) if isinstance(not_resource.raw, List) else not_resource

            if actions:
                yield from get_wildcard_nodes(actions, WILDCARD_ACTION)
            if resources:
                yield from get_wildcard_nodes(resources, WILDCARD_RESOURCE)


def _has_admin_access(managed_policies: Node) -> Iterator[Node]:
    if managed_policies:
        for man_pol in managed_policies.data:
            # IAM role should not have AdministratorAccess policy
            if "AdministratorAccess" in man_pol.raw:
                yield man_pol


def _cfn_iam_is_role_over_privileged_iter_vulns(
    file_ext: str,
    iam_iterator: Iterator[Union[AWSIamManagedPolicy, Node]],
) -> Iterator[Union[AWSIamManagedPolicy, Node]]:
    for iam_res in iam_iterator:
        managed_policies = iam_res.inner.get("ManagedPolicyArns")
        yield from _has_admin_access(managed_policies)

        policies = iam_res.inner.get("Policies")
        yield from _check_policy_documents(policies, file_ext)

        if assume_role_policy := iam_res.inner.get("AssumeRolePolicyDocument"):
            yield from _check_assume_role_policies(
                assume_role_policy, file_ext
            )


def cfn_kms_key_has_master_keys_exposed_to_everyone(
    content: str, path: str, template: Any
) -> Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        cwe={FindingEnum.F325.value.cwe},
        description_key=(
            "src.lib_path.f325.kms_key_has_master_keys_exposed_to_everyone"
        ),
        finding=FindingEnum.F325,
        iterator=get_cloud_iterator(
            _cfn_kms_key_has_master_keys_exposed_to_everyone_iter_vulns(
                keys_iterator=iter_kms_keys(template=template),
            )
        ),
        path=path,
        developer=DeveloperEnum.ALEJANDRO_TRUJILLO,
    )


def cfn_iam_has_wildcard_resource_on_write_action(
    content: str, path: str, template: Any
) -> Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        cwe={FindingEnum.F325.value.cwe},
        description_key=(
            "src.lib_path.f325.iam_has_wildcard_resource_on_write_action"
        ),
        finding=FindingEnum.F325,
        iterator=get_cloud_iterator(
            _cfn_iam_has_wildcard_resource_on_write_action_iter_vulns(
                iam_iterator=iter_iam_managed_policies_and_roles(
                    template=template
                ),
            )
        ),
        path=path,
        developer=DeveloperEnum.ALEJANDRO_TRUJILLO,
    )


def cfn_iam_is_policy_miss_configured(
    content: str, file_ext: str, path: str, template: Any
) -> Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        cwe={FindingEnum.F325.value.cwe},
        description_key=("src.lib_path.f325.iam_is_policy_miss_configured"),
        finding=FindingEnum.F325,
        iterator=get_cloud_iterator(
            _cfn_iam_is_policy_miss_configured_iter_vulns(
                file_ext=file_ext,
                iam_iterator=iter_iam_managed_policies_and_mgd_policies(
                    template=template
                ),
            )
        ),
        path=path,
        developer=DeveloperEnum.ALEJANDRO_TRUJILLO,
    )


def cfn_iam_has_privileges_over_iam(
    content: str, path: str, template: Any
) -> Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        cwe={FindingEnum.F325.value.cwe},
        description_key=("src.lib_path.f325.iam_has_privileges_over_iam"),
        finding=FindingEnum.F325,
        iterator=get_cloud_iterator(
            _cfn_iam_has_privileges_over_iam_iter_vulns(
                iam_iterator=iter_iam_managed_policies_and_roles(
                    template=template
                ),
            )
        ),
        path=path,
        developer=DeveloperEnum.ALEJANDRO_TRUJILLO,
    )


def cfn_iam_is_role_over_privileged(
    content: str, file_ext: str, path: str, template: Any
) -> Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        cwe={FindingEnum.F325.value.cwe},
        description_key=("src.lib_path.f325.iam_is_role_over_privileged"),
        finding=FindingEnum.F325,
        iterator=get_cloud_iterator(
            _cfn_iam_is_role_over_privileged_iter_vulns(
                file_ext=file_ext,
                iam_iterator=iter_iam_roles(template=template),
            )
        ),
        path=path,
        developer=DeveloperEnum.ALEJANDRO_TRUJILLO,
    )
