# Standard
from typing import cast, List

# Third party
from graphql.type.definition import GraphQLResolveInfo

# Local
from backend import authz
from backend.decorators import enforce_group_level_auth_async
from backend.typing import Project as Group


@enforce_group_level_auth_async
async def resolve(
    parent: Group,
    _info: GraphQLResolveInfo,
    **_kwargs: None
) -> List[str]:
    group_name: str = cast(str, parent['name'])

    return sorted(await authz.get_group_service_attributes(group_name))
