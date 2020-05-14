import random
from backend.dal import internal_project as internal_project_dal
from backend.exceptions import EmptyPoolProjectName


def does_project_name_exist(project_name: str) -> bool:
    return project_name in internal_project_dal.get_all_project_names()


def get_project_name() -> str:
    list_project_name = internal_project_dal.get_all_project_names()
    if not list_project_name:
        raise EmptyPoolProjectName()
    return random.choice(list_project_name)


def remove_project_name(project_name: str) -> bool:
    return internal_project_dal.remove_project_name(project_name)
