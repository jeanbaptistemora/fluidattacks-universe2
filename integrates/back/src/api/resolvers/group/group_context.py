from .schema import (
    GROUP,
)
from db_model.groups.types import (
    Group,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)


@GROUP.field("groupContext")
def resolve(
    parent: Group,
    _info: GraphQLResolveInfo,
) -> str | None:
    return parent.context
