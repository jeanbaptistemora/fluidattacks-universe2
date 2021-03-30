# Standard
from typing import cast

# Third party
from graphql.type.definition import GraphQLResolveInfo

# Local
from backend.typing import Project as Group
from organizations import domain as orgs_domain


async def resolve(
    parent: Group,
    _info: GraphQLResolveInfo,
    **_kwargs: None
) -> str:
    group_name: str = cast(str, parent['name'])
    org_id: str = await orgs_domain.get_id_for_group(group_name)

    return cast(str, await orgs_domain.get_name_by_id(org_id))
