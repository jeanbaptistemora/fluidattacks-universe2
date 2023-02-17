from .schema import (
    ORGANIZATION,
)
from db_model.constants import (
    DEFAULT_MAX_SEVERITY,
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


@ORGANIZATION.field("maxAcceptanceSeverity")
async def resolve(
    parent: Organization,
    _info: GraphQLResolveInfo,
    **_kwargs: None,
) -> Decimal:
    return (
        parent.policies.max_acceptance_severity
        if parent.policies.max_acceptance_severity is not None
        else DEFAULT_MAX_SEVERITY
    )
