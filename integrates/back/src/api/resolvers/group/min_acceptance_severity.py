from db_model.constants import (
    DEFAULT_MIN_SEVERITY,
)
from db_model.organizations.types import (
    Organization,
)
from decimal import (
    Decimal,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)


async def resolve(
    parent: Organization,
    info: GraphQLResolveInfo,
    **_kwargs: None,
) -> Decimal:
    if parent.policies:
        return parent.policies.min_acceptance_severity or DEFAULT_MIN_SEVERITY

    organization: Organization = await info.context.loaders.organization.load(
        parent.organization_id
    )
    return (
        organization.policies.min_acceptance_severity or DEFAULT_MIN_SEVERITY
    )
