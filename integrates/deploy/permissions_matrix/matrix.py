import authz
from pandas import (
    DataFrame,
)
from typing import (
    Dict,
    List,
    Set,
)


def create_dataframe(
    dataset: Dict[str, List[str]],
    columns: List[str],
    rows: List[str],
    filename: str,
) -> None:
    dataframe = DataFrame(dataset, columns=columns, index=rows)
    html_matrix = dataframe.to_html()

    with open(
        "deploy/permissions_matrix/" + filename + ".html",
        "w",
        encoding="utf-8",
    ) as text_file:
        text_file.write(html_matrix)


def fill_matrix(
    roles_and_permissions: Dict[str, Dict[str, Set[str]]],
    columns: List[str],
    all_actions: List[str],
) -> Dict[str, List[str]]:
    dataset = {}
    for role in columns:
        values = []
        for action in all_actions:
            is_action = (
                "X"
                if action in roles_and_permissions[role]["actions"]
                else " "
            )
            values.append(is_action)
        dataset[role] = values
    return dataset


def get_matrix_parameters(
    roles_and_permissions: Dict[str, Dict[str, Set[str]]], filename: str
) -> None:
    all_actions = []
    columns = list(roles_and_permissions.keys())
    roles_lenght = {}
    for role in columns:
        role_actions = roles_and_permissions[role]["actions"]
        roles_lenght[role] = len(role_actions)
        for action in role_actions:
            all_actions.append(action)
    all_actions = sorted(set(all_actions))
    sorted_columns = sorted(
        roles_lenght.keys(), key=lambda k: roles_lenght[k], reverse=True
    )
    dataset = fill_matrix(roles_and_permissions, sorted_columns, all_actions)
    pattern = "api_resolvers_"
    rows = [
        action.replace(pattern, "") if pattern in action else action
        for action in all_actions
    ]

    create_dataframe(dataset, sorted_columns, rows, filename)


# Matrix for common permissions
get_matrix_parameters(authz.GROUP_LEVEL_ROLES, "group_level")
get_matrix_parameters(authz.ORGANIZATION_LEVEL_ROLES, "organization_level")
get_matrix_parameters(authz.USER_LEVEL_ROLES, "user_level")

# Matrix for fluid users permissions
get_matrix_parameters(
    authz.GROUP_LEVEL_ROLES_FOR_FLUIDATTACKS, "group_level_for_fluidattacks"
)
get_matrix_parameters(
    authz.ORGANIZATION_LEVEL_ROLES_FOR_FLUIDATTACKS,
    "organization_level_for_fluidattacks",
)
get_matrix_parameters(
    authz.USER_LEVEL_ROLES_FOR_FLUIDATTACKS, "user_level_for_fluidattacks"
)
