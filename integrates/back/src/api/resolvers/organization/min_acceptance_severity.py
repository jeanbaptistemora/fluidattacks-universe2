from db_model.organization.types import (
    Organization,
)
from decimal import (
    Decimal,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from typing import (
    Any,
    Union,
)

DEFAULT_MIN_SEVERITY = Decimal("0.0")


async def resolve(
    parent: Union[Organization, dict[str, Any]],
    _info: GraphQLResolveInfo,
    **_kwargs: None,
) -> Decimal:
    if isinstance(parent, dict):
        return (
            parent["min_acceptance_severity"]
            if "min_acceptance_severity" in parent
            else DEFAULT_MIN_SEVERITY
        )

    return parent.policies.min_acceptance_severity or DEFAULT_MIN_SEVERITY
