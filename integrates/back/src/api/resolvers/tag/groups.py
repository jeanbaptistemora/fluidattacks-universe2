from custom_types import (
    Tag,
)
from dataloaders import (
    Dataloaders,
)
from db_model.groups.types import (
    Group,
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
    Tuple,
)


async def resolve(
    parent: Tag, info: GraphQLResolveInfo, **_kwargs: None
) -> Tuple[Group, ...]:
    group_names: List[str] = get_key_or_fallback(parent, "groups", "projects")
    loaders: Dataloaders = info.context.loaders
    groups: Tuple[Group, ...] = await loaders.group_typed.load_many(
        tuple(group_names)
    )
    return groups_domain.filter_active_groups_new(groups)
