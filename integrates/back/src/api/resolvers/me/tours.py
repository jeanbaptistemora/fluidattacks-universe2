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
) -> Dict[str, bool]:
    user_email = str(parent["user_email"])
    data: dict = await stakeholders_domain.get_by_email(user_email)

    return data["tours"]
