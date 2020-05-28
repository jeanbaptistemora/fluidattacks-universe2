from backend.dal import available_group as available_group_dal


def exists(group_name: str) -> bool:
    return available_group_dal.exists(group_name)


def get_name() -> str:
    return available_group_dal.get_one()


def remove(group_name: str) -> bool:
    return available_group_dal.remove(group_name)
