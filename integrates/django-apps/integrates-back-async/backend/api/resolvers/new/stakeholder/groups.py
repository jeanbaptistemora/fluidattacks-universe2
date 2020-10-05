# Standard
import asyncio
from typing import cast, Dict, List

# Third party
from aiodataloader import DataLoader
from graphql.type.definition import GraphQLResolveInfo

# Local
from backend.api.resolvers import project as old_resolver
from backend.domain import user as user_domain
from backend.typing import Project as Group, Stakeholder
from backend.utils import aio


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

    # Temporary while migrating group resolvers
    return cast(
        List[Group],
        await aio.materialize(
            old_resolver.resolve(
                info,
                cast(Dict[str, str], group)['name'],
                selection_set=info.field_nodes[0].selection_set
            )
            for group in groups
        )
    )
