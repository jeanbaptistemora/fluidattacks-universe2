from .schema import (
    GROUP,
)
from db_model.groups.types import (
    Group,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from typing import (
    Optional,
)


@GROUP.field("paymentId")
async def resolve(
    parent: Group,
    _info: GraphQLResolveInfo,
) -> Optional[str]:
    return str(parent.state.payment_id)
