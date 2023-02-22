from .schema import (
    GROUP,
)
from db_model.groups.types import (
    Group,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)


@GROUP.field("tags")
async def resolve(
    parent: Group,
    _info: GraphQLResolveInfo,
) -> list[str] | None:
    return list(parent.state.tags) if parent.state.tags else None
