import random
from backend.dal import internal_project as internal_project_dal
from backend.exceptions import EmptyPoolProjectName


def get_project_name():
    list_project_name = internal_project_dal.get_all_project_names()
    if not list_project_name:
        raise EmptyPoolProjectName()
    return random.choice(list_project_name)
