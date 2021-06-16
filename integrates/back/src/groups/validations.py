from custom_exceptions import (
    GroupNotFound,
)
from custom_types import (
    Group,
)


def group_exist(group: Group) -> Group:
    if not group.get("has_integrates"):
        raise GroupNotFound()

    return group
