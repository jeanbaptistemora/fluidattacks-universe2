from db_model.organization.types import (
    Organization,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from newutils.utils import (
    get_key_or_fallback,
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
        max_number_acceptances = get_key_or_fallback(
            parent,
            "max_number_acceptances",
            "max_number_acceptations",
        )
        return (
            int(max_number_acceptances)
            if max_number_acceptances is not None
            else None
        )

    return parent.policies.max_number_acceptances
