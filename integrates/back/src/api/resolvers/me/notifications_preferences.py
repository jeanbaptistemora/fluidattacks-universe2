from dataloaders import (
    Dataloaders,
)
from db_model.stakeholders.types import (
    NotificationsPreferences,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from stakeholders.domain import (
    get_stakeholder,
)
from typing import (
    Any,
)


async def resolve(
    parent: dict[str, Any], info: GraphQLResolveInfo, **_kwargs: None
) -> NotificationsPreferences:
    loaders: Dataloaders = info.context.loaders
    email = str(parent["user_email"])
    stakeholder = await get_stakeholder(loaders, email)

    return stakeholder.state.notifications_preferences
