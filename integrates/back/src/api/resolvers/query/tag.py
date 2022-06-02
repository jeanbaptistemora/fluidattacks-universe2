from aioextensions import (
    collect,
)
from custom_exceptions import (
    TagNotFound,
)
from dataloaders import (
    Dataloaders,
)
from db_model.groups.types import (
    Group,
)
from db_model.organizations.types import (
    Organization,
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
from tags import (
    domain as tags_domain,
)
from typing import (
    Any,
    Dict,
)


@require_login
async def resolve(
    _parent: None, info: GraphQLResolveInfo, **kwargs: str
) -> Dict[str, Any]:
    loaders: Dataloaders = info.context.loaders
    tag_name: str = kwargs["tag"].lower()
    user_data: dict[str, str] = await token_utils.get_jwt_content(info.context)
    user_email: str = user_data["user_email"]
    user_group_names: list[str] = await groups_domain.get_groups_by_user(
        loaders, user_email
    )
    are_valid_groups = await collect(
        tuple(
            groups_domain.is_valid(loaders, group_name)
            for group_name in user_group_names
        )
    )
    group_names_filtered = [
        group_name
        for group_name, is_valid in zip(user_group_names, are_valid_groups)
        if is_valid
    ]

    if group_names_filtered:
        group: Group = await loaders.group.load(group_names_filtered[0])
        org_id: str = group.organization_id
        organization: Organization = await loaders.organization.load(org_id)
        org_name: str = organization.name

        allowed_tags: list[str] = await tags_domain.filter_allowed_tags(
            loaders, org_name, group_names_filtered
        )
        if tag_name in allowed_tags:
            tag = await tags_domain.get_attributes(org_name, tag_name)
            return {
                "name": tag["tag"],
                "last_closing_vuln": tag["last_closing_date"],
                **tag,
            }
    raise TagNotFound()
