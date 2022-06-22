from graphql.type.definition import (
    GraphQLResolveInfo,
)
from stakeholders import (
    domain as stakeholders_domain,
)
from typing import (
    Any,
    Dict,
    Optional,
)


async def resolve(
    parent: Dict[str, Any], _info: GraphQLResolveInfo, **_kwargs: None
) -> Optional[str]:
    user_email = str(parent["user_email"])
    user_info: dict = await stakeholders_domain.get_by_email(user_email)
    return user_info["phone"]
