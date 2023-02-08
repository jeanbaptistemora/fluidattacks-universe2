from ariadne.utils import (
    convert_kwargs_to_snake_case,
)
from dataloaders import (
    Dataloaders,
)
from db_model.events.types import (
    Event,
    GroupEventsRequest,
)
from decorators import (
    concurrent_decorators,
    enforce_group_level_auth_async,
    require_asm,
    require_login,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)


@convert_kwargs_to_snake_case
@concurrent_decorators(
    require_login,
    enforce_group_level_auth_async,
    require_asm,
)
async def resolve(
    _parent: None, info: GraphQLResolveInfo, **kwargs: str
) -> list[Event]:
    loaders: Dataloaders = info.context.loaders
    group_name = kwargs["group_name"].lower()

    return await loaders.group_events.load(
        GroupEventsRequest(group_name=group_name)
    )
