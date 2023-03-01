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


@TOE_LINES.field("attackedLines")
@enforce_group_level_auth_async
def resolve(
    parent: ToeLines, _info: GraphQLResolveInfo, **_kwargs: None
) -> int:
    return parent.state.attacked_lines
