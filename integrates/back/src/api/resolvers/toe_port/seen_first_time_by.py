from .schema import (
    TOE_PORT,
)
from db_model.toe_ports.types import (
    ToePort,
)
from decorators import (
    enforce_group_level_auth_async,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from typing import (
    Optional,
)


@TOE_PORT.field("seenFirstTimeBy")
@enforce_group_level_auth_async
async def resolve(
    parent: ToePort, _info: GraphQLResolveInfo, **_kwargs: None
) -> Optional[str]:
    return parent.seen_first_time_by
