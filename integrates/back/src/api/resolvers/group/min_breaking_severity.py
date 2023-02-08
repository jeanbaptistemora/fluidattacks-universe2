from dataloaders import (
    Dataloaders,
)
from db_model.constants import (
    DEFAULT_MIN_SEVERITY,
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


async def resolve(
    parent: Group,
    info: GraphQLResolveInfo,
    **_kwargs: None,
) -> Decimal:
    if parent.policies:
        return parent.policies.min_breaking_severity or DEFAULT_MIN_SEVERITY

    loaders: Dataloaders = info.context.loaders
    organization = await orgs_utils.get_organization(
        loaders, parent.organization_id
    )

    return organization.policies.min_breaking_severity or DEFAULT_MIN_SEVERITY
