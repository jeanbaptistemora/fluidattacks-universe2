from db_model.constants import (
    DEFAULT_MAX_SEVERITY,
)
from db_model.groups.types import (
    Group,
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
    parent: Group,
    info: GraphQLResolveInfo,
    **_kwargs: None,
) -> Decimal:
    if parent.policies:
        return parent.policies.max_acceptance_severity or DEFAULT_MAX_SEVERITY

    organization: Organization = await info.context.loaders.organization.load(
        parent.organization_id
    )
    return (
        organization.policies.max_acceptance_severity or DEFAULT_MAX_SEVERITY
    )
