# Standard
from typing import cast

# Third party
from graphql.type.definition import GraphQLResolveInfo

# Local
from backend.domain import organization as org_domain
from backend.typing import Project as Group


async def resolve(
    parent: Group,
    _info: GraphQLResolveInfo,
    **_kwargs: None
) -> str:
    group_name: str = cast(str, parent['name'])
    org_id: str = await org_domain.get_id_for_group(group_name)

    return await org_domain.get_name_by_id(org_id)
