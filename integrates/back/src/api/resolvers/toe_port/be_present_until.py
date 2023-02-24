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


@TOE_PORT.field("bePresentUntil")
@enforce_group_level_auth_async
def resolve(
    parent: ToePort, _info: GraphQLResolveInfo, **_kwargs: None
) -> datetime | None:
    return parent.state.be_present_until
