from .schema import (
    GROUP,
)
from db_model.groups.enums import (
    GroupManaged,
)
from db_model.groups.types import (
    Group,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)


@GROUP.field("managed")
def resolve(
    parent: Group,
    _info: GraphQLResolveInfo,
) -> GroupManaged:
    return parent.state.managed
