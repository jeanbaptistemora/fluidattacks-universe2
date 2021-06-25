from aiodataloader import (
    DataLoader,
)
from custom_types import (
    Group,
    Tag,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from groups import (
    domain as groups_domain,
)
from newutils.utils import (
    resolve_kwargs,
)
from typing import (
    cast,
    List,
)


async def resolve(
    parent: Tag, info: GraphQLResolveInfo, **_kwargs: None
) -> List[Group]:
    group_names: str = cast(str, resolve_kwargs(parent, "groups", "projects"))
    group_loader: DataLoader = info.context.loaders.group
    groups: List[Group] = await group_loader.load_many(group_names)
    groups_filtered = groups_domain.filter_active_groups(groups)

    return groups_filtered
