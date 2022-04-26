from aioextensions import (
    collect,
)
import authz
from contextlib import (
    suppress,
)
from custom_types import (
    Tag as TagType,
)
from db_model.groups.types import (
    Group,
)
from decimal import (
    Decimal,
)
from organizations import (
    domain as orgs_domain,
)
from tags import (
    dal as tags_dal,
)
from typing import (
    Any,
    Optional,
    Union,
)


async def delete(organization_name: str, tag: str) -> bool:
    return await tags_dal.delete(organization_name, tag)


async def filter_allowed_tags(
    loaders: Any,
    organization_name: str,
    user_group_names: list[str],
) -> list[str]:
    groups: tuple[Group, ...] = await loaders.group_typed.load_many(
        user_group_names
    )
    all_tags = {
        str(tag).lower()
        for group in groups
        if group.tags
        for tag in group.tags
    }
    are_tags_allowed = await collect(
        is_tag_allowed(groups, organization_name, tag) for tag in all_tags
    )
    tags = [
        tag
        for tag, is_tag_allowed in zip(all_tags, are_tags_allowed)
        if is_tag_allowed
    ]
    return tags


async def get_attributes(
    organization: str, tag: str, attributes: Optional[list[str]] = None
) -> dict[str, Union[list[str], str]]:
    return await tags_dal.get_attributes(organization, tag, attributes)


async def get_tags(
    organization: str, attributes: Optional[list[str]] = None
) -> list[TagType]:
    return await tags_dal.get_tags(organization, attributes)


async def has_user_access(email: str, subject: str) -> bool:
    with suppress(ValueError):
        org_id, portfolio = subject.split("PORTFOLIO#")
        organization_name = await orgs_domain.get_name_by_id(org_id)
        portfolio_info = await get_attributes(
            organization_name, portfolio, ["projects"]
        )
        portfolio_groups: list[str] = list(portfolio_info.get("projects", []))
        org_access, group_access = await collect(
            (
                orgs_domain.has_user_access(
                    email=email, organization_id=org_id
                ),
                authz.get_group_level_roles(
                    email=email,
                    groups=portfolio_groups,
                ),
            )
        )
        return org_access and any(group_access.values())
    raise ValueError("Invalid subject")


async def is_tag_allowed(
    user_groups: tuple[Group, ...],
    organization_name: str,
    tag: str,
) -> bool:
    all_groups_tag = await get_attributes(organization_name, tag, ["projects"])
    user_groups_tag = [
        group.name
        for group in user_groups
        if group.tags and tag in [p_tag.lower() for p_tag in group.tags]
    ]
    return any(
        group in user_groups_tag
        for group in all_groups_tag.get("projects", [])
    )


async def update(
    organization_name: str,
    tag: str,
    data: dict[str, Union[list[str], Decimal]],
) -> bool:
    return await tags_dal.update(organization_name, tag, data)
