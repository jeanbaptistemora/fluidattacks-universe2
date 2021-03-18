# Standard
from typing import cast, Dict, List

# Third party
from aiodataloader import DataLoader
from graphql.type.definition import GraphQLResolveInfo

# Local
from backend import util
from backend.typing import Organization, Project as Group
from users import domain as users_domain


async def resolve(
    parent: Organization,
    info: GraphQLResolveInfo,
    **_kwargs: None
) -> List[Group]:
    user_info: Dict[str, str] = await util.get_jwt_content(info.context)
    user_email: str = user_info['user_email']
    org_id: str = cast(str, parent['id'])

    user_groups: List[str] = await users_domain.get_projects(
        user_email,
        organization_id=org_id
    )

    group_loader: DataLoader = info.context.loaders.group
    groups: List[Group] = await group_loader.load_many(user_groups)

    return groups
