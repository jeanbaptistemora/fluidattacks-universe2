from dataloaders import (
    Dataloaders,
)
from db_model.groups.types import (
    Group,
)
from decimal import (
    Decimal,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from organizations import (
    utils as orgs_utils,
)
from typing import (
    Optional,
)


async def resolve(
    parent: Group,
    info: GraphQLResolveInfo,
    **_kwargs: None,
) -> Optional[Decimal]:
    if parent.policies:
        return parent.policies.min_breaking_severity

    loaders: Dataloaders = info.context.loaders
    organization = await orgs_utils.get_organization(
        loaders, parent.organization_id
    )

    return organization.policies.min_breaking_severity
