import authz
from custom_exceptions import (
    InvalidParameter,
)
from custom_types import (
    Me,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from typing import (
    cast,
    Tuple,
)


async def resolve(parent: Me, _info: GraphQLResolveInfo, **kwargs: str) -> str:
    user_email: str = cast(str, parent["user_email"])
    entity: str = kwargs["entity"]
    identifier: str = kwargs.get("identifier", "")
    role = ""
    group_entities: Tuple = ("GROUP", "PROJECT")

    if entity == "USER":
        role = await authz.get_user_level_role(user_email)
    elif entity in group_entities and identifier:
        role = await authz.get_group_level_role(user_email, identifier)
    elif entity == "ORGANIZATION" and identifier:
        role = await authz.get_organization_level_role(user_email, identifier)
    else:
        raise InvalidParameter()
    return role
