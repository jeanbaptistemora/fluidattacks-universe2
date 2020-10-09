# Standard
import asyncio
from typing import cast, List

# Third party
from aiodataloader import DataLoader
from graphql.type.definition import GraphQLResolveInfo

# Local
from backend.domain import user as user_domain
from backend.typing import Project as Group, Stakeholder


async def resolve(
    parent: Stakeholder,
    info: GraphQLResolveInfo,
    **_kwargs: None
) -> List[Group]:
    email: str = cast(str, parent['email'])

    active_task = asyncio.create_task(user_domain.get_projects(email))
    inactive_task = asyncio.create_task(
        user_domain.get_projects(email, active=False)
    )
    active, inactive = tuple(await asyncio.gather(active_task, inactive_task))
    user_groups: List[str] = active + inactive

    group_loader: DataLoader = info.context.loaders['group']
    groups: List[Group] = await group_loader.load_many(user_groups)

    return groups
