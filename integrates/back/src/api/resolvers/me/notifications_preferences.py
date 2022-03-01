from custom_types import (
    Me,
)
from db_model.users.get import (
    User,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from typing import (
    Dict,
    List,
)


async def resolve(
    parent: Me, info: GraphQLResolveInfo, **_kwargs: None
) -> List[Dict[str, str]]:
    user_email: str = parent["user_email"]
    user: User = await info.context.loaders.user.load(user_email)

    return user.notifications_preferences
