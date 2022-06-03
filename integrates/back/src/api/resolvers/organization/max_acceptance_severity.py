from db_model.organizations.types import (
    Organization,
)
from decimal import (
    Decimal,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)

DEFAULT_MAX_SEVERITY = Decimal("10.0")


async def resolve(
    parent: Organization,
    _info: GraphQLResolveInfo,
    **_kwargs: None,
) -> Decimal:
    return parent.policies.max_acceptance_severity or DEFAULT_MAX_SEVERITY
