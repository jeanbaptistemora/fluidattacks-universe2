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
    get_key_or_fallback,
)
from typing import (
    List,
)


async def resolve(
    parent: Tag, info: GraphQLResolveInfo, **_kwargs: None
) -> List[Group]:
    group_names: str = get_key_or_fallback(parent, "groups", "projects")
    group_loader: DataLoader = info.context.loaders.group
    groups: List[Group] = await group_loader.load_many(group_names)
    groups_filtered = groups_domain.filter_active_groups(groups)

    return groups_filtered
