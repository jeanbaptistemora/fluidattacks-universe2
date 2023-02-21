from collections.abc import (
    Iterator,
)


def is_public_principal(principals: Iterator[str] | str) -> bool:
    principal_list = (
        principals if isinstance(principals, list) else [principals]
    )
    if "*" in principal_list:
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
