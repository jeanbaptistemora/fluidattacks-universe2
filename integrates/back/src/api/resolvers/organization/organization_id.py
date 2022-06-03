from db_model.organizations.types import (
    Organization,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from newutils.organizations import (
    add_org_id_prefix,
)


async def resolve(
    parent: Organization,
    _info: GraphQLResolveInfo,
    **_kwargs: None,
) -> str:
    organization_id = parent.id

    # Currently, the api expects the prefix in the id
    return add_org_id_prefix(organization_id)
