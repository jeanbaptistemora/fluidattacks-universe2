from dataloaders import (
    Dataloaders,
)
from db_model.events.types import (
    Event,
)
from event_comments import (
    domain as event_comments_domain,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from newutils import (
    token as token_utils,
)
from newutils.event_comments import (
    format_event_consulting_resolve,
)
from typing import (
    Any,
)


async def resolve(
    parent: Event,
    info: GraphQLResolveInfo,
    **_kwargs: None,
) -> list[dict[str, Any]]:
    loaders: Dataloaders = info.context.loaders
    user_data: dict[str, str] = await token_utils.get_jwt_content(info.context)
    event_coments = await event_comments_domain.get_comments(
        loaders, parent.group_name, parent.id, user_data["user_email"]
    )

    return [
        format_event_consulting_resolve(comment) for comment in event_coments
    ]
