# pylint: disable=import-error

from typing import Dict, List, Set

from backend import authz

from pandas import DataFrame


def create_dataframe(dataset: Dict[str, List[str]], columns: List[str],
                     rows: List[str], filename: str):
    dataframe = DataFrame(dataset, columns=columns, index=rows)
    html_matrix = dataframe.to_html()
    text_file = open("deploy/permissions-matrix/" + filename + ".html", "w")
    text_file.write(html_matrix)
    text_file.close()


def fill_matrix(
        roles_and_permissions: Dict[str, Dict[str, Set[str]]],
        columns: List[str], all_actions: List[str]) -> Dict[str, List[str]]:
    dataset = {}
    for role in columns:
        values = []
        for action in all_actions:
            is_action = ('X'
                         if action
                         in roles_and_permissions.get(role).get('actions')
                         else ' ')
            values.append(is_action)
        dataset[role] = values
    return dataset


def get_matrix_parameters(
        roles_and_permissions: Dict[str, Dict[str, Set[str]]], filename: str):
    all_actions = []
    columns = list(roles_and_permissions.keys())
    roles_lenght = {}
    for role in columns:
        role_actions = roles_and_permissions.get(role).get('actions')
        roles_lenght[role] = len(role_actions)
        for action in role_actions:
            all_actions.append(action)
    all_actions = sorted(set(all_actions))
    sorted_columns = sorted(
        roles_lenght.keys(), key=lambda k: roles_lenght[k], reverse=True)
    dataset = fill_matrix(roles_and_permissions, sorted_columns, all_actions)
    pattern = 'backend_api_resolvers_'
    rows = [action.replace(pattern, '') if pattern in action else action
            for action in all_actions]

    create_dataframe(dataset, sorted_columns, rows, filename)


get_matrix_parameters(authz.GROUP_LEVEL_ROLES, 'group_level')
get_matrix_parameters(authz.USER_LEVEL_ROLES, 'user_level')
