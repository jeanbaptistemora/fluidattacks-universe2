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
)


async def resolve(parent: Me, _info: GraphQLResolveInfo, **kwargs: str) -> str:
    # As Entity is no longer a required arg, this check is needed to keep
    # backwards compatibility while enforcing the need for a non-null
    # identifier if the entity is not USER
    if (
        "entity" in kwargs
        and kwargs.get("entity") != "USER"
        and "identifier" not in kwargs
    ):
        raise InvalidParameter()

    user_email: str = cast(str, parent["user_email"])
    entity: str = kwargs.get("entity", "USER")
    identifier: str = kwargs.get("identifier", "")
    role = ""
    group_entities = {"GROUP", "PROJECT"}

    if entity == "USER":
        role = await authz.get_user_level_role(user_email)
    elif entity in group_entities and identifier:
        role = await authz.get_group_level_role(user_email, identifier)
    elif entity == "ORGANIZATION" and identifier:
        role = await authz.get_organization_level_role(user_email, identifier)
    else:
        raise InvalidParameter()
    return role
