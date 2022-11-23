from db_model.groups.enums import (
    GroupTier,
)
from db_model.groups.types import (
    Group,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)


async def resolve(
    parent: Group,
    _info: GraphQLResolveInfo,
) -> GroupTier:
    return parent.state.tier
