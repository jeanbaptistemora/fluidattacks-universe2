from .schema import (
    TOE_PORT,
)
from datetime import (
    datetime,
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


@TOE_PORT.field("attackedAt")
@enforce_group_level_auth_async
async def resolve(
    parent: ToePort, _info: GraphQLResolveInfo, **_kwargs: None
) -> Optional[datetime]:
    return parent.state.attacked_at
