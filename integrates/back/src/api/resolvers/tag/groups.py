from dataloaders import (
    Dataloaders,
)
from db_model.groups.types import (
    Group,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from newutils import (
    groups as groups_utils,
)
from newutils.utils import (
    get_key_or_fallback,
)
from typing import (
    Any,
    Dict,
    List,
    Tuple,
)


async def resolve(
    parent: Dict[str, Any], info: GraphQLResolveInfo, **_kwargs: None
) -> Tuple[Group, ...]:
    group_names: List[str] = get_key_or_fallback(parent, "groups", "projects")
    loaders: Dataloaders = info.context.loaders
    groups: Tuple[Group, ...] = await loaders.group_typed.load_many(
        tuple(group_names)
    )
    return groups_utils.filter_active_groups(groups)
