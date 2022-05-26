from db_model.groups.types import (
    Group,
)
from db_model.organizations.types import (
    Organization,
)
from typing import (
    Any,
)


async def get_organization_name(loaders: Any, group_name: str) -> str:
    group: Group = await loaders.group_typed.load(group_name)
    organization: Organization = await loaders.organization_typed.load(
        group.organization_id
    )
    return organization.name
