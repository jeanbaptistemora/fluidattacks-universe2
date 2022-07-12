from db_model.groups.enums import (
    GroupStateStatus,
)
from db_model.groups.types import (
    Group,
)
from db_model.organizations.types import (
    Organization,
)
from typing import (
    Any,
    Optional,
)


def filter_active_groups(groups: tuple[Group, ...]) -> tuple[Group, ...]:
    return tuple(
        group
        for group in groups
        if group.state.status == GroupStateStatus.ACTIVE
    )


def filter_deleted_groups(groups: tuple[Group, ...]) -> tuple[Group, ...]:
    return tuple(
        group
        for group in groups
        if group.state.status == GroupStateStatus.DELETED
    )


async def get_group_max_acceptance_days(
    *, loaders: Any, group: Group
) -> Optional[int]:
    if group.policies:
        return group.policies.max_acceptance_days

    organization: Organization = await loaders.organization.load(
        group.organization_id
    )
    return organization.policies.max_acceptance_days
