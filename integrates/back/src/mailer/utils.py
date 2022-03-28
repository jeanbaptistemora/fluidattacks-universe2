from db_model.groups.types import (
    Group,
)
from typing import (
    Any,
)


async def get_organization_name(loaders: Any, group_name: str) -> str:
    group: Group = await loaders.group_typed.load(group_name)
    return group.organization_name
