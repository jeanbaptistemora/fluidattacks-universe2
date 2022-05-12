from db_model.organizations.types import (
    Organization,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from newutils.organizations import (
    add_org_id_prefix,
)
from typing import (
    Any,
    Union,
)


async def resolve(
    parent: Union[Organization, dict[str, Any]],
    _info: GraphQLResolveInfo,
    **_kwargs: None,
) -> str:
    organization_id = parent["id"] if isinstance(parent, dict) else parent.id

    # Currently, the api expects the prefix in the id
    return add_org_id_prefix(organization_id)
