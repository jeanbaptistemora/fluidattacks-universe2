from .schema import (
    TOE_INPUT,
)
from db_model.toe_inputs.types import (
    ToeInput,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from typing import (
    Optional,
)


@TOE_INPUT.field("hasVulnerabilities")
async def resolve(
    parent: ToeInput, _info: GraphQLResolveInfo, **_kwargs: None
) -> Optional[bool]:
    return parent.state.has_vulnerabilities
