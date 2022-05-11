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
    Any,
    Union,
)

DEFAULT_MAX_SEVERITY = Decimal("10.0")


async def resolve(
    parent: Union[Organization, dict[str, Any]],
    _info: GraphQLResolveInfo,
    **_kwargs: None,
) -> Decimal:
    if isinstance(parent, dict):
        return (
            parent["max_acceptance_severity"]
            if "max_acceptance_severity" in parent
            else DEFAULT_MAX_SEVERITY
        )

    return parent.policies.max_acceptance_severity or DEFAULT_MAX_SEVERITY
