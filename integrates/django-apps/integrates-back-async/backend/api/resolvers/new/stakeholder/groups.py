# Standard
import asyncio
from typing import cast, List

# Third party
from ariadne.utils import convert_kwargs_to_snake_case
from graphql.type.definition import GraphQLResolveInfo

# Local
from backend.domain import project as group_domain, user as user_domain
from backend.typing import Project as Group, Stakeholder
from backend.utils import aio


@convert_kwargs_to_snake_case
async def resolve(
    parent: Stakeholder,
    _info: GraphQLResolveInfo,
    **_kwargs: str
) -> List[Group]:
    email: str = cast(str, parent['email'])

    active_task = asyncio.create_task(user_domain.get_projects(email))
    inactive_task = asyncio.create_task(
        user_domain.get_projects(email, active=False)
    )
    active, inactive = tuple(await asyncio.gather(active_task, inactive_task))
    user_groups: List[str] = active + inactive

    groups: List[Group] = cast(
        List[Group],
        await aio.materialize(
            group_domain.get_by_name(group)
            for group in user_groups
        )
    )

    return groups
