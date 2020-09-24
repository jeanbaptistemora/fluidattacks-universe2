# Standard
from typing import cast, Dict, List

# Third party
from aiodataloader import DataLoader
from ariadne.utils import convert_kwargs_to_snake_case
from graphql.type.definition import GraphQLResolveInfo

# Local
from backend import util
from backend.domain import user as user_domain
from backend.typing import Organization, Project as Group


@convert_kwargs_to_snake_case
async def resolve(
    parent: Organization,
    info: GraphQLResolveInfo,
    **_kwargs: str
) -> List[Group]:
    user_info: Dict[str, str] = await util.get_jwt_content(info.context)
    user_email: str = user_info['user_email']
    org_id: str = cast(str, parent['id'])

    user_groups: List[str] = await user_domain.get_projects(
        user_email,
        organization_id=org_id
    )

    group_loader: DataLoader = info.context.loaders['project']
    groups: List[Group] = group_loader.load_many(user_groups)

    return groups
