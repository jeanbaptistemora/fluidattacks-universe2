from db_model.organizations.types import (
    Organization,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from typing import (
    Any,
    Union,
)

ORGANIZATION_ID_PREFIX = "ORG#"


async def resolve(
    parent: Union[Organization, dict[str, Any]],
    _info: GraphQLResolveInfo,
    **_kwargs: None,
) -> str:
    organization_id = parent["id"] if isinstance(parent, dict) else parent.id

    # Currently, the api expects the prefix in the id
    return (
        organization_id
        if organization_id.startswith(ORGANIZATION_ID_PREFIX)
        else f"{ORGANIZATION_ID_PREFIX}{organization_id}"
    )
