from typing import (
    Any,
)


async def get_organization_name(loaders: Any, group_name: str) -> str:
    group_loader = loaders.group
    group = await group_loader.load(group_name)
    org_id = group["organization"]

    organization_loader = loaders.organization
    organization = await organization_loader.load(org_id)
    return organization["name"]
