from .schema import (
    ME,
)
import authz
from dataloaders import (
    Dataloaders,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from typing import (
    Any,
)


@ME.field("role")
async def resolve(
    parent: dict[str, Any], info: GraphQLResolveInfo, **_kwargs: str
) -> str:
    loaders: Dataloaders = info.context.loaders
    user_email = str(parent["user_email"])
    return await authz.get_user_level_role(loaders, user_email)
