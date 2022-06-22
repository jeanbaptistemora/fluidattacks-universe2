from graphql.type.definition import (
    GraphQLResolveInfo,
)
from stakeholders import (
    domain as stakeholders_domain,
)
from typing import (
    Any,
    Dict,
)


async def resolve(
    parent: Dict[str, Any], _info: GraphQLResolveInfo, **_kwargs: None
) -> bool:
    user_email = str(parent["user_email"])
    remember: bool = bool(
        await stakeholders_domain.get_data(user_email, "legal_remember")
    )
    return remember
