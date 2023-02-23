from aws.iam.structure import (
    is_resource_permissive,
)
from aws.iam.utils import (
    match_pattern,
)
from collections.abc import (
    Iterator,
)
from lib_root.utilities.terraform import (
    get_attribute,
)
from model.graph_model import (
    Graph,
    NId,
)
import re


def match_iam_passrole(action: str) -> bool:
    return match_pattern(action, "iam:PassRole")


def aux_open_passrole_iterate_vulnerabilities(
    resources: list, actions: list
) -> bool:
    if all(
        (
            any(map(match_iam_passrole, actions)),
            any(map(is_resource_permissive, resources)),
        )
    ):
        return True
    return False


def _iam_user_missing_role_based_security(
    graph: Graph, nid: NId
) -> NId | None:
    expected_attr = get_attribute(graph, nid, "name")
    if expected_attr[0]:
        return expected_attr[2]
    return None


def is_public_principal(principals: Iterator[str] | str) -> bool:
    principal_list = (
        principals if isinstance(principals, list) else [principals]
    )
    if "*" in principal_list:
        return True
    return False


def action_has_full_access_to_ssm(actions: str | list) -> bool:
    actions_list = actions if isinstance(actions, list) else [actions]
    for action in actions_list:
        if action == "ssm:*":
            return True
    return False


def is_s3_action_writeable(actions: list | str) -> bool:
    actions_list = actions if isinstance(actions, list) else [actions]
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
    for action in actions_list:
        if any(action.startswith(f"s3:{atw}") for atw in action_start_with):
            return True
    return False


def check_resource_name(
    managed_policies_iterator: Iterator[str],
    name_resource: str,
) -> bool:
    if any(
        policy.startswith("aws_iam_role")
        and policy.split(".")[1] == name_resource
        for policy in managed_policies_iterator
    ):
        return True
    return False


def check_role_name(
    managed_policies_iterator: Iterator[str],
    role_iterator: Iterator[tuple[str, str]],
    name_role: str,
) -> bool:
    if any(
        (res_name := attr[1])
        and check_resource_name(managed_policies_iterator, res_name)
        and (role_name := attr[0])
        and role_name in name_role
        for attr in role_iterator
    ):
        return True
    return False


def action_has_attach_role(
    actions: str | list,
    resources: str | list,
    managed_policies_iterator: Iterator[str],
    role_iterator: Iterator[tuple[str, str]],
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
