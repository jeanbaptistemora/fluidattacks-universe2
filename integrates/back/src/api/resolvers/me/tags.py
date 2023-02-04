from aioextensions import (
    collect,
)
from ariadne.utils import (
    convert_kwargs_to_snake_case,
)
from dataloaders import (
    Dataloaders,
)
from db_model.portfolios.types import (
    Portfolio,
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
from organizations.utils import (
    get_organization,
)
from typing import (
    Any,
)


@convert_kwargs_to_snake_case
@require_organization_access
async def resolve(
    parent: dict[str, Any],
    info: GraphQLResolveInfo,
    **kwargs: str,
) -> list[Portfolio]:
    loaders: Dataloaders = info.context.loaders
    organization_tags_loader = loaders.organization_portfolios
    user_email = str(parent["user_email"])
    organization_id: str = kwargs["organization_id"]

    organization = await get_organization(loaders, organization_id)
    org_tags = await organization_tags_loader.load(organization.name)
    user_groups = await groups_domain.get_groups_by_stakeholder(
        loaders, user_email, organization_id=organization_id
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
        tag
        for tag in org_tags
        if any(group in groups_filtered for group in tag.groups)
    ]
