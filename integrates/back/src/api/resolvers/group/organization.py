from db_model.groups.types import (
    Group,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from organizations import (
    domain as orgs_domain,
)


async def resolve(
    parent: Group,
    _info: GraphQLResolveInfo,
) -> str:
    return await orgs_domain.get_name_by_id(parent.organization_id)
