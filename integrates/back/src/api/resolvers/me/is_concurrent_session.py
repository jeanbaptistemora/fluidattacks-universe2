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
    is_concurrent_session: bool = bool(
        await stakeholders_domain.get_data(user_email, "is_concurrent_session")
    )
    return is_concurrent_session
