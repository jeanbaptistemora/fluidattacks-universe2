from aioextensions import (
    collect,
)
import authz
from contextlib import (
    suppress,
)
from db_model.groups.types import (
    Group,
)
from db_model.organizations.types import (
    Organization,
)
from db_model.portfolios.constants import (
    OLD_GROUPS,
)
from decimal import (
    Decimal,
)
from organizations import (
    domain as orgs_domain,
)
from tags import (
    dal,
)
from typing import (
    Any,
    Dict,
    Optional,
    Union,
)


async def delete(organization_name: str, tag: str) -> bool:
    return await dal.delete(organization_name, tag)


async def filter_allowed_tags(
    loaders: Any,
    organization_name: str,
    user_group_names: list[str],
) -> list[str]:
    groups: tuple[Group, ...] = await loaders.group.load_many(user_group_names)
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
    return await dal.get_attributes(organization, tag, attributes)


async def get_tags(
    organization: str, attributes: Optional[list[str]] = None
) -> list[Dict[str, Any]]:
    return await dal.get_tags(organization, attributes)


async def has_user_access(loaders: Any, email: str, subject: str) -> bool:
    with suppress(ValueError):
        org_id, portfolio = subject.split("PORTFOLIO#")
        organization: Organization = await loaders.organization_typed.load(
            org_id
        )
        organization_name = organization.name
        portfolio_info = await get_attributes(
            organization_name, portfolio, [OLD_GROUPS]
        )
        portfolio_groups: list[str] = list(portfolio_info.get(OLD_GROUPS, []))
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
    all_groups_tag = await get_attributes(organization_name, tag, [OLD_GROUPS])
    user_groups_tag = [
        group.name
        for group in user_groups
        if group.tags and tag in [p_tag.lower() for p_tag in group.tags]
    ]
    return any(
        group in user_groups_tag
        for group in all_groups_tag.get(OLD_GROUPS, [])
    )


async def update(
    organization_name: str,
    tag: str,
    data: dict[str, Union[list[str], Decimal]],
) -> bool:
    return await dal.update(organization_name, tag, data)
