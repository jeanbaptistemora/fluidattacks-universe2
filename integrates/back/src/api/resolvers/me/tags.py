from aioextensions import (
    collect,
)
from ariadne.utils import (
    convert_kwargs_to_snake_case,
)
from dataloaders import (
    Dataloaders,
)
from decorators import (
    require_organization_access,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from groups import (
    domain as groups_domain,
)
from typing import (
    Any,
    cast,
    Dict,
)


@convert_kwargs_to_snake_case
@require_organization_access
async def resolve(
    parent: Dict[str, Any],
    info: GraphQLResolveInfo,
    **kwargs: str,
) -> list[Dict[str, Any]]:
    loaders: Dataloaders = info.context.loaders
    organization_loader = loaders.organization
    organization_tags_loader = loaders.organization_tags
    user_email = str(parent["user_email"])
    organization_id: str = kwargs["organization_id"]

    organization = await organization_loader.load(organization_id)
    org_tags = await organization_tags_loader.load(organization["name"])
    user_groups = await groups_domain.get_groups_by_user(
        user_email, organization_id=organization_id
    )
    are_valid_groups = await collect(
        tuple(groups_domain.is_valid(loaders, group) for group in user_groups)
    )
    groups_filtered = [
        group
        for group, is_valid in zip(user_groups, are_valid_groups)
        if is_valid
    ]

    return [
        {
            "name": tag["tag"],
            "last_closing_vuln": tag["last_closing_date"],
            **tag,
        }
        for tag in org_tags
        if any(
            group in groups_filtered
            for group in cast(list[str], tag["groups"])
        )
    ]
