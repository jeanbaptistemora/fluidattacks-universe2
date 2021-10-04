# pylint: disable=unsubscriptable-object
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
from decimal import (
    Decimal,
)
from groups import (
    domain as groups_domain,
)
from newutils.utils import (
    get_key_or_fallback,
)
from organizations import (
    domain as orgs_domain,
)
from tags import (
    dal as tags_dal,
)
from typing import (
    cast,
    Dict,
    List,
    Optional,
    Union,
)


async def delete(organization: str, tag: str) -> bool:
    return await tags_dal.delete(organization, tag)


async def filter_allowed_tags(
    organization: str, user_groups: List[str]
) -> List[str]:
    groups = await collect(
        groups_domain.get_attributes(group, ["tag", "project_name"])
        for group in user_groups
    )
    all_tags = {
        str(tag.lower()) for group in groups for tag in group.get("tag", [])
    }
    are_tags_allowed = await collect(
        is_tag_allowed(groups, organization, tag) for tag in all_tags
    )
    tags = [
        tag
        for tag, is_tag_allowed in zip(all_tags, are_tags_allowed)
        if is_tag_allowed
    ]
    return tags


async def get_attributes(
    organization: str, tag: str, attributes: Optional[List[str]] = None
) -> Dict[str, Union[List[str], str]]:
    return await tags_dal.get_attributes(organization, tag, attributes)


async def get_tags(
    organization: str, attributes: Optional[List[str]] = None
) -> List[TagType]:
    return await tags_dal.get_tags(organization, attributes)


async def has_user_access(email: str, subject: str) -> bool:
    with suppress(ValueError):
        org_id, portfolio = subject.split("PORTFOLIO#")
        org_name = await orgs_domain.get_name_by_id(org_id)
        portfolio_info = await get_attributes(
            org_name, portfolio, ["projects"]
        )
        org_access, group_access = await collect(
            (
                orgs_domain.has_user_access(
                    email=email, organization_id=org_id
                ),
                authz.get_group_level_roles(
                    email=email,
                    groups=cast(List[str], portfolio_info.get("projects", [])),
                ),
            )
        )
        return org_access and any(group_access.values())
    raise ValueError("Invalid subject")


async def is_tag_allowed(
    user_groups: List[Dict[str, Union[str, List[str]]]],
    organization: str,
    tag: str,
) -> bool:
    all_groups_tag = await get_attributes(organization, tag, ["projects"])
    user_groups_tag = [
        str(get_key_or_fallback(group, fallback="")).lower()
        for group in user_groups
        if tag in [p_tag.lower() for p_tag in group.get("tag", [])]
    ]
    return any(
        group.lower() in user_groups_tag
        for group in all_groups_tag.get("projects", [])
    )


async def update(
    organization: str, tag: str, data: Dict[str, Union[List[str], Decimal]]
) -> bool:
    return await tags_dal.update(organization, tag, data)
