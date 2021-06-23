from custom_exceptions import (
    GroupNotFound,
)
from custom_types import (
    Group,
)


def group_exist(group: Group) -> Group:
    has_asm: bool = group.get("has_asm", False) or group.get(
        "has_integrates", False
    )
    if not has_asm:
        raise GroupNotFound()

    return group
