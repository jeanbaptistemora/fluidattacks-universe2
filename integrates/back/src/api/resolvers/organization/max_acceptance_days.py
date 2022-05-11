from db_model.organizations.types import (
    Organization,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from typing import (
    Any,
    Optional,
    Union,
)


async def resolve(
    parent: Union[Organization, dict[str, Any]],
    _info: GraphQLResolveInfo,
    **_kwargs: None,
) -> Optional[int]:
    if isinstance(parent, dict):
        return (
            int(parent["max_acceptance_days"])
            if "max_acceptance_days" in parent
            and parent.get("max_acceptance_days") is not None
            else None
        )

    return parent.policies.max_acceptance_days
