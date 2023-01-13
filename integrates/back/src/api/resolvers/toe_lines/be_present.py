from db_model.toe_lines.types import (
    ToeLines,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)


async def resolve(
    parent: ToeLines, _info: GraphQLResolveInfo, **_kwargs: None
) -> bool:
    return parent.be_present
