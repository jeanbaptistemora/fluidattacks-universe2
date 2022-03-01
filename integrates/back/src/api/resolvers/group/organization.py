from db_model.groups.types import (
    Group,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from organizations import (
    domain as orgs_domain,
)
from typing import (
    Any,
    Dict,
    Union,
)


async def resolve(
    parent: Union[Group, Dict[str, Any]],
    _info: GraphQLResolveInfo,
    **_kwargs: Any,
) -> str:
    if isinstance(parent, dict):
        group_name: str = parent["name"]
        org_id: str = await orgs_domain.get_id_for_group(group_name)
        return str(await orgs_domain.get_name_by_id(org_id))

    return parent.organization_name
