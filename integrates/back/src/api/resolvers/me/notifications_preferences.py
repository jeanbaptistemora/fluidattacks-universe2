from db_model.users.types import (
    NotificationsPreferences,
    User,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from typing import (
    Any,
    Dict,
)


async def resolve(
    parent: Dict[str, Any], info: GraphQLResolveInfo, **_kwargs: None
) -> NotificationsPreferences:
    user_email = str(parent["user_email"])
    user: User = await info.context.loaders.user.load(user_email)

    return user.notifications_preferences
