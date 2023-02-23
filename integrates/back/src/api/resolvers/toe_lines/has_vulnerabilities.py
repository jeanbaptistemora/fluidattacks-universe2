from .schema import (
    TOE_LINES,
)
from db_model.toe_lines.types import (
    ToeLines,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)


@TOE_LINES.field("hasVulnerabilities")
async def resolve(
    parent: ToeLines, _info: GraphQLResolveInfo, **_kwargs: None
) -> bool | None:
    return parent.state.has_vulnerabilities
