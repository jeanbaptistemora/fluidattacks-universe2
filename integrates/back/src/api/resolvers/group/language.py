from .schema import (
    GROUP,
)
from db_model.groups.types import (
    Group,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)


@GROUP.field("language")
async def resolve(
    parent: Group,
    _info: GraphQLResolveInfo,
) -> str:
    return parent.language.value
