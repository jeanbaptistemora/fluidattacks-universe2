# Standard
from typing import (
    Dict,
    List,
    cast,
)

# Third party
from aiodataloader import DataLoader
from graphql.type.definition import GraphQLResolveInfo

# Local
from backend.typing import (
    Organization,
    Project as Group,
)
from groups import domain as groups_domain
from newutils import token as token_utils


async def resolve(
    parent: Organization,
    info: GraphQLResolveInfo,
    **_kwargs: None
) -> List[Group]:
    user_info: Dict[str, str] = await token_utils.get_jwt_content(info.context)
    user_email: str = user_info['user_email']

    org_id: str = cast(str, parent['id'])
    user_groups: List[str] = await groups_domain.get_groups_by_user(
        user_email,
        organization_id=org_id
    )

    group_loader: DataLoader = info.context.loaders.group
    groups: List[Group] = await group_loader.load_many(user_groups)
    return groups
