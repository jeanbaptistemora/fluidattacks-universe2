from .schema import (
    TOE_INPUT,
)
from db_model.toe_inputs.types import (
    ToeInput,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)


@TOE_INPUT.field("hasVulnerabilities")
def resolve(
    parent: ToeInput, _info: GraphQLResolveInfo, **_kwargs: None
) -> bool | None:
    return parent.state.has_vulnerabilities
