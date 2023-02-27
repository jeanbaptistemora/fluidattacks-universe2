from .schema import (
    TAG,
)
from dataloaders import (
    Dataloaders,
)
from db_model.groups.types import (
    Group,
)
from db_model.portfolios.types import (
    Portfolio,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from newutils import (
    groups as groups_utils,
)


@TAG.field("groups")
async def resolve(
    parent: Portfolio,
    info: GraphQLResolveInfo,
    **_kwargs: None,
) -> list[Group]:
    group_names = parent.groups
    loaders: Dataloaders = info.context.loaders
    groups = await loaders.group.load_many(group_names)

    return groups_utils.filter_active_groups(groups)
