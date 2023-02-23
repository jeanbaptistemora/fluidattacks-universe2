from .schema import (
    TOE_LINES,
)
from db_model.toe_lines.types import (
    SortsSuggestion,
    ToeLines,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)


@TOE_LINES.field("sortsSuggestions")
async def resolve(
    parent: ToeLines, _info: GraphQLResolveInfo, **_kwargs: None
) -> list[SortsSuggestion] | None:
    return parent.state.sorts_suggestions
