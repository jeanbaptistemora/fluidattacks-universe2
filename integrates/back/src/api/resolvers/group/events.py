from .schema import (
    GROUP,
)
from dataloaders import (
    Dataloaders,
)
from db_model.events.types import (
    Event,
    GroupEventsRequest,
)
from db_model.groups.types import (
    Group,
)
from decorators import (
    concurrent_decorators,
    enforce_group_level_auth_async,
    require_asm,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)


@GROUP.field("events")
@concurrent_decorators(
    enforce_group_level_auth_async,
    require_asm,
)
async def resolve(
    parent: Group,
    info: GraphQLResolveInfo,
    **_kwargs: None,
) -> list[Event]:
    loaders: Dataloaders = info.context.loaders
    events_group = await loaders.group_events.load(
        GroupEventsRequest(group_name=parent.name)
    )

    return events_group
