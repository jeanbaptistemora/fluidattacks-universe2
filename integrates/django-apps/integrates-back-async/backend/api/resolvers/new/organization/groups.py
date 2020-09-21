# Standard
from typing import cast, Dict, List

# Third party
from ariadne.utils import convert_kwargs_to_snake_case
from graphql.type.definition import GraphQLResolveInfo

# Local
from backend import util
from backend.domain import project as group_domain, user as user_domain
from backend.typing import Organization, Project as Group
from backend.utils import aio


@convert_kwargs_to_snake_case
async def resolve(
    obj: Organization,
    info: GraphQLResolveInfo,
    **_kwargs: str
) -> List[Group]:
    user_info: Dict[str, str] = await util.get_jwt_content(info.context)
    user_email: str = user_info['user_email']
    org_id: str = cast(str, obj['id'])

    user_groups: List[str] = await user_domain.get_projects(
        user_email,
        organization_id=org_id
    )

    groups: List[Group] = cast(
        List[Group],
        await aio.materialize(
            group_domain.get_by_name(group)
            for group in user_groups
        )
    )

    return groups
