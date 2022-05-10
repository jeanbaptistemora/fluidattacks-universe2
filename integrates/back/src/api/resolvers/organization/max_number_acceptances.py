from db_model.organization.types import (
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
            int(parent["max_number_acceptances"])
            if "max_number_acceptances" in parent
            and parent.get("max_number_acceptances") is not None
            else None
        )

    return parent.policies.max_number_acceptances
