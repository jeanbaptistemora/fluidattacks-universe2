from backend.dal import available_group as internal_project_dal
from backend.exceptions import EmptyPoolProjectName


def does_project_name_exist(project_name: str) -> bool:
    return internal_project_dal.exists(project_name)


def get_project_name() -> str:
    project_name = internal_project_dal.get_one()
    if not project_name:
        raise EmptyPoolProjectName()
    return project_name


def remove_project_name(project_name: str) -> bool:
    return internal_project_dal.remove(project_name)
