from .schema import (
    TOE_LINES,
)
from db_model.toe_lines.types import (
    ToeLines,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)


@TOE_LINES.field("loc")
def resolve(
    parent: ToeLines, _info: GraphQLResolveInfo, **_kwargs: None
) -> int:
    return parent.state.loc
