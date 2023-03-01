from .schema import (
    GROUP,
)
from db_model.groups.types import (
    Group,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)


@GROUP.field("hasMachine")
def resolve(
    parent: Group,
    _info: GraphQLResolveInfo,
) -> bool:
    return parent.state.has_machine
