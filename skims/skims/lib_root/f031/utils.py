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
