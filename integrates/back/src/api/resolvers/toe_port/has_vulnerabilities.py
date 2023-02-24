from .schema import (
    TOE_PORT,
)
from db_model.toe_ports.types import (
    ToePort,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)


@TOE_PORT.field("hasVulnerabilities")
def resolve(
    parent: ToePort, _info: GraphQLResolveInfo, **_kwargs: None
) -> bool | None:
    return parent.state.has_vulnerabilities
