from .schema import (
    GROUP,
)
from db_model.groups.types import (
    Group,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)


@GROUP.field("service")
def resolve(
    parent: Group,
    _info: GraphQLResolveInfo,
) -> str | None:
    if parent.state.service:
        return parent.state.service.value
    return None
