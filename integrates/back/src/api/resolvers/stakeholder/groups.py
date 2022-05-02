from aioextensions import (
    collect,
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
from newutils import (
    groups as groups_utils,
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
    email = str(parent["email"])
    active, inactive = await collect(
        [
            groups_domain.get_groups_by_user(email),
            groups_domain.get_groups_by_user(email, active=False),
        ]
    )
    user_groups: List[str] = active + inactive

    loaders: Dataloaders = info.context.loaders
    groups: Tuple[Group, ...] = await loaders.group_typed.load_many(
        user_groups
    )
    return groups_utils.filter_active_groups(groups)
