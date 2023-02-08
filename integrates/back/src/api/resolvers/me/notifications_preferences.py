from dataloaders import (
    Dataloaders,
)
from db_model.stakeholders.types import (
    NotificationsPreferences,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from typing import (
    Any,
)


async def resolve(
    parent: dict[str, Any], info: GraphQLResolveInfo, **_kwargs: None
) -> NotificationsPreferences:
    loaders: Dataloaders = info.context.loaders
    email = str(parent["user_email"])
    stakeholder = await loaders.stakeholder.load(email)

    return stakeholder.state.notifications_preferences
