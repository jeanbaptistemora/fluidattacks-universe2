# Standard
import asyncio
from typing import cast, Dict, List

# Third party
from aiodataloader import DataLoader
from ariadne.utils import convert_kwargs_to_snake_case
from graphql.type.definition import GraphQLResolveInfo

# Local
from backend.api.resolvers import project as old_resolver
from backend.decorators import (
    concurrent_decorators,
    enforce_user_level_auth_async,
    require_login,
)
from backend.domain import user as user_domain
from backend.typing import Project as Group
from backend.utils import aio


@convert_kwargs_to_snake_case
@concurrent_decorators(
    require_login,
    enforce_user_level_auth_async,
)
async def resolve(
    _parent: None,
    info: GraphQLResolveInfo,
    **kwargs: str
) -> List[Group]:
    user_email: str = kwargs['user_email']

    active_task = asyncio.create_task(user_domain.get_projects(user_email))
    inactive_task = asyncio.create_task(
        user_domain.get_projects(user_email, active=False)
    )
    active, inactive = tuple(await asyncio.gather(active_task, inactive_task))
    user_groups = active + inactive

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
