
from typing import (
    List,
    cast,
)

from aiodataloader import DataLoader
from aioextensions import collect
from graphql.type.definition import GraphQLResolveInfo

from custom_types import (
    Project as Group,
    Stakeholder,
)
from groups import domain as groups_domain


async def resolve(
    parent: Stakeholder,
    info: GraphQLResolveInfo,
    **_kwargs: None
) -> List[Group]:
    email: str = cast(str, parent['email'])
    active, inactive = await collect([
        groups_domain.get_groups_by_user(email),
        groups_domain.get_groups_by_user(email, active=False)
    ])
    user_groups: List[str] = active + inactive

    group_loader: DataLoader = info.context.loaders.group
    groups: List[Group] = await group_loader.load_many(user_groups)
    return groups
