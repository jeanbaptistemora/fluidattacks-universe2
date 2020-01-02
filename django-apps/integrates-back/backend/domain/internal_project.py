import random
from backend.dal import internal_project as internal_project_dal


def get_project_name():
    return random.choice(internal_project_dal.get_all_project_names())
