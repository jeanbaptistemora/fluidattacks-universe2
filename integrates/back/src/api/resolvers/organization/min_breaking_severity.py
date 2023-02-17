from .schema import (
    ORGANIZATION,
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
from typing import (
    Optional,
)


@ORGANIZATION.field("minBreakingSeverity")
async def resolve(
    parent: Organization,
    _info: GraphQLResolveInfo,
    **_kwargs: None,
) -> Optional[Decimal]:
    return parent.policies.min_breaking_severity
