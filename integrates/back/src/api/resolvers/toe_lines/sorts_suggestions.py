from db_model.toe_lines.types import (
    SortsSuggestion,
    ToeLines,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from typing import (
    Optional,
)


async def resolve(
    parent: ToeLines, _info: GraphQLResolveInfo, **_kwargs: None
) -> Optional[list[SortsSuggestion]]:
    return parent.sorts_suggestions
