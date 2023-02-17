from .schema import (
    ORGANIZATION,
)
from dataloaders import (
    Dataloaders,
)
from db_model.organizations.types import (
    Organization,
    OrganizationUnreliableIndicators,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)


@ORGANIZATION.field("coveredRepositories")
async def resolve(
    parent: Organization,
    info: GraphQLResolveInfo,
    **_kwargs: None,
) -> int:
    loaders: Dataloaders = info.context.loaders
    org_indicators: OrganizationUnreliableIndicators = (
        await loaders.organization_unreliable_indicators.load(parent.id)
    )

    return (
        org_indicators.covered_repositories
        if org_indicators.covered_repositories
        else 0
    )
