from .schema import (
    TOE_PORT,
)
from db_model.toe_ports.types import (
    ToePort,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from typing import (
    Optional,
)


@TOE_PORT.field("hasVulnerabilities")
async def resolve(
    parent: ToePort, _info: GraphQLResolveInfo, **_kwargs: None
) -> Optional[bool]:
    return parent.state.has_vulnerabilities
