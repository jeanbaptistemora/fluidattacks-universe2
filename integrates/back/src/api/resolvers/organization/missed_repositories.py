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


@ORGANIZATION.field("missedRepositories")
async def resolve(
    parent: Organization,
    info: GraphQLResolveInfo,
    **_kwargs: None,
) -> int:
    loaders: Dataloaders = info.context.loaders
    indicators: OrganizationUnreliableIndicators = (
        await loaders.organization_unreliable_indicators.load(parent.id)
    )

    return (
        indicators.missed_repositories if indicators.missed_repositories else 0
    )
