from dataloaders import (
    Dataloaders,
)
from db_model.events.types import (
    Event,
)
from db_model.groups.types import (
    Group,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)


async def resolve(
    parent: Event,
    info: GraphQLResolveInfo,
    **_kwargs: None,
) -> str:
    loaders: Dataloaders = info.context.loaders
    group_name = parent.group_name
    group: Group = await loaders.group.load(group_name)

    return group.state.type.value
