from .schema import (
    GROUP,
)
from db_model.groups.enums import (
    GroupStateStatus,
)
from db_model.groups.types import (
    Group,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)


@GROUP.field("userDeletion")
async def resolve(
    parent: Group,
    _info: GraphQLResolveInfo,
) -> str | None:
    return (
        parent.state.modified_by
        if parent.state.status == GroupStateStatus.DELETED
        else None
    )
