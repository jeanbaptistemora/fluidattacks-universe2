from db_model.organizations.types import (
    Organization,
)
from decimal import (
    Decimal,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)

DEFAULT_MIN_SEVERITY = Decimal("0.0")


async def resolve(
    parent: Organization,
    _info: GraphQLResolveInfo,
    **_kwargs: None,
) -> Decimal:
    return parent.policies.min_acceptance_severity or DEFAULT_MIN_SEVERITY
