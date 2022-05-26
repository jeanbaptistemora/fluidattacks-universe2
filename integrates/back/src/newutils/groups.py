from db_model.groups.enums import (
    GroupStateStatus,
)
from db_model.groups.types import (
    Group,
)


def filter_active_groups(groups: tuple[Group, ...]) -> tuple[Group, ...]:
    return tuple(
        group
        for group in groups
        if group.state.status == GroupStateStatus.ACTIVE
    )
