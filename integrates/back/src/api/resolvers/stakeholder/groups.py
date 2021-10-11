from aiodataloader import (
    DataLoader,
)
from aioextensions import (
    collect,
)
from custom_types import (
    Group,
    Stakeholder,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from groups import (
    domain as groups_domain,
)
from typing import (
    List,
)


async def resolve(
    parent: Stakeholder, info: GraphQLResolveInfo, **_kwargs: None
) -> List[Group]:
    email: str = parent["email"]
    active, inactive = await collect(
        [
            groups_domain.get_groups_by_user(email),
            groups_domain.get_groups_by_user(email, active=False),
        ]
    )
    user_groups: List[str] = active + inactive

    group_loader: DataLoader = info.context.loaders.group
    groups: List[Group] = await group_loader.load_many(user_groups)
    groups_filtered = groups_domain.filter_active_groups(groups)

    return groups_filtered
