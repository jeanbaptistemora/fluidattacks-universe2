from .schema import (
    GROUP,
)
from db_model.groups.types import (
    Group,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)


@GROUP.field("paymentId")
def resolve(
    parent: Group,
    _info: GraphQLResolveInfo,
) -> str | None:
    return str(parent.state.payment_id)
