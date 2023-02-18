from .schema import (
    TOE_LINES,
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


@TOE_LINES.field("comments")
@enforce_group_level_auth_async
async def resolve(
    parent: ToeLines, _info: GraphQLResolveInfo, **_kwargs: None
) -> str:
    return parent.state.comments
