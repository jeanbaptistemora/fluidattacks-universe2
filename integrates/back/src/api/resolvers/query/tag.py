from aioextensions import (
    collect,
)
from custom_exceptions import (
    TagNotFound,
)
from custom_types import (
    Tag,
)
from decorators import (
    require_login,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from groups import (
    domain as groups_domain,
)
from newutils import (
    token as token_utils,
)
from organizations import (
    domain as orgs_domain,
)
from tags import (
    domain as tags_domain,
)
from typing import (
    Dict,
    List,
)


@require_login
async def resolve(
    _parent: None, info: GraphQLResolveInfo, **kwargs: str
) -> Tag:
    tag_name: str = kwargs["tag"].lower()

    user_data: Dict[str, str] = await token_utils.get_jwt_content(info.context)
    user_email: str = user_data["user_email"]
    user_groups: List[str] = await groups_domain.get_groups_by_user(user_email)
    are_alive_groups = await collect(
        tuple(groups_domain.is_alive(group) for group in user_groups)
    )
    groups_filtered = [
        group
        for group, is_alive in zip(user_groups, are_alive_groups)
        if is_alive
    ]

    if groups_filtered:
        org_id: str = await orgs_domain.get_id_for_group(groups_filtered[0])
        org_name: str = await orgs_domain.get_name_by_id(org_id)

        allowed_tags: List[str] = await tags_domain.filter_allowed_tags(
            org_name, groups_filtered
        )
        if tag_name in allowed_tags:
            tag = await tags_domain.get_attributes(org_name, tag_name)
            return {
                "name": tag["tag"],
                "last_closing_vuln": tag["last_closing_date"],
                **tag,
            }
    raise TagNotFound()
