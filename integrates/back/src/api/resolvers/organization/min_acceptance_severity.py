from .schema import (
    ORGANIZATION,
)
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


@ORGANIZATION.field("minAcceptanceSeverity")
async def resolve(
    parent: Organization,
    _info: GraphQLResolveInfo,
    **_kwargs: None,
) -> Decimal:
    return parent.policies.min_acceptance_severity or DEFAULT_MIN_SEVERITY
