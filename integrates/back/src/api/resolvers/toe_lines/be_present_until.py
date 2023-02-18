from .schema import (
    TOE_LINES,
)
from datetime import (
    datetime,
)
from db_model.toe_lines.types import (
    ToeLines,
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


@TOE_LINES.field("bePresentUntil")
@enforce_group_level_auth_async
async def resolve(
    parent: ToeLines, _info: GraphQLResolveInfo, **_kwargs: None
) -> Optional[datetime]:
    return parent.state.be_present_until
