from collections.abc import (
    Iterable,
    Iterator,
)
from lib_path.common import (
    get_cloud_iterator,
    get_vulnerabilities_from_iterator_blocking,
)
from metaloaders.model import (
    Node,
)
from model.core_model import (
    MethodsEnum,
    Vulnerabilities,
)
from parse_hcl2.common import (
    get_attribute,
    get_tree_value,
    iterate_resources,
)
from parse_hcl2.structure.aws import (
    iterate_iam_policy_documents as terraform_iterate_iam_policy_documents,
    iterate_managed_policy_arns as terraform_iterate_managed_policy_arns,
)
import re
from typing import (
    Any,
)


def check_resource_name(
    managed_policies_iterator: Iterator[Any],
    name_resource: str,
) -> bool:
    if any(
        not isinstance(policy.data[0], str)
        and (value := str(get_tree_value(policy.data[0])))
        and value.startswith("aws_iam_role")
        and value.split(".")[1] == name_resource
        for policy in managed_policies_iterator
    ):
        return True
    return False


def check_role_name(
    managed_policies_iterator: Iterator[Any],
    role_iterator: Iterator[Any],
    name_role: str,
) -> bool:
    if any(
        len(attr.namespace) > 1
        and (res_name := attr.namespace[2])
        and check_resource_name(managed_policies_iterator, res_name)
        and (role_name := get_attribute(attr.body, "name"))
        and role_name.val in name_role
        for attr in role_iterator
    ):
        return True
    return False


def action_has_attach_role(
    actions: str | Iterable[str],
    resources: str | Iterable[str],
    managed_policies_iterator: Iterator[Any],
    role_iterator: Iterator[Any],
) -> bool:
    actions_list = actions if isinstance(actions, list) else [actions]
    resource_list = resources if isinstance(resources, list) else [resources]
    for action in actions_list:
        if action == "iam:Attach*" and any(
            re.split("::", res)[0].startswith("arn:aws:iam")
            and re.search(r"\$?[A-Za-z0-9_./{}]:role/", res)
            and (
                check_role_name(
                    managed_policies_iterator,
                    role_iterator,
                    re.split(":role/", res)[1],
                )
            )
            for res in resource_list
        ):
            return True
    return False


def _tfm_iam_role_excessive_privilege(
    managed_policies_iterator: Iterator[Any],
    statements_iterator: Iterator[Any],
    role_iterator: Iterator[Any],
) -> Iterator[Any]:
    for stmt in statements_iterator:
        stmt_raw = (
            stmt.raw
            if isinstance(stmt, Node) and hasattr(stmt, "raw")
            else stmt.data
        )
        resources = stmt_raw.get("Resource", [])
        actions = stmt_raw.get("Action", [])
        if action_has_attach_role(
            actions, resources, managed_policies_iterator, role_iterator
        ):
            yield stmt


def tfm_iam_excessive_role_policy(
    content: str, path: str, model: Any
) -> Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        description_key="src.lib_path.f031.iam_excessive_role_policy",
        iterator=get_cloud_iterator(
            _tfm_iam_role_excessive_privilege(
                managed_policies_iterator=(
                    terraform_iterate_managed_policy_arns(model=model)
                ),
                statements_iterator=terraform_iterate_iam_policy_documents(
                    model=model,
                ),
                role_iterator=iterate_resources(
                    model, "resource", "aws_iam_role"
                ),
            )
        ),
        path=path,
        method=MethodsEnum.TFM_IAM_EXCESSIVE_ROLE_POLICY,
    )
