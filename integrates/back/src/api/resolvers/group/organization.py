from db_model.groups.types import (
    Group,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)


async def resolve(
    parent: Group,
    _info: GraphQLResolveInfo,
) -> str:
    return parent.organization_name
