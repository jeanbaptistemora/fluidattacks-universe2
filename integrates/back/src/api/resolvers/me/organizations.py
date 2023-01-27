from dataloaders import (
    Dataloaders,
)
from db_model.organizations.types import (
    Organization,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from newutils import (
    organizations as orgs_utils,
)
from typing import (
    Any,
)


async def resolve(
    parent: dict[str, Any],
    info: GraphQLResolveInfo,
    **_kwargs: None,
) -> tuple[Organization, ...]:
    loaders: Dataloaders = info.context.loaders
    user_email = str(parent["user_email"])
    stakeholder_orgs = await loaders.stakeholder_organizations_access.load(
        user_email
    )
    organization_ids: list[str] = [
        org.organization_id for org in stakeholder_orgs
    ]
    organizations = await loaders.organization.load_many(organization_ids)

    return orgs_utils.filter_active_organizations(tuple(organizations))
