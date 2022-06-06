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
from newutils.utils import (
    get_key_or_fallback,
)
from typing import (
    Any,
    Dict,
    Tuple,
    Union,
)


async def resolve(
    parent: Union[Dict[str, Any], Portfolio],
    info: GraphQLResolveInfo,
    **_kwargs: None,
) -> Tuple[Group, ...]:
    if isinstance(parent, dict):
        group_names: set[str] = get_key_or_fallback(
            parent, "groups", "projects"
        )
    else:
        group_names = parent.groups
    loaders: Dataloaders = info.context.loaders
    groups: Tuple[Group, ...] = await loaders.group.load_many(
        tuple(group_names)
    )
    return groups_utils.filter_active_groups(groups)
