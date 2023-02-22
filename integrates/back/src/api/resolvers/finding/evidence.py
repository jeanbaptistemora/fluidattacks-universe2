from .schema import (
    FINDING,
)
from db_model.findings.types import (
    Finding,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from newutils.findings import (
    get_formatted_evidence,
)


@FINDING.field("evidence")
def resolve(
    parent: Finding, _info: GraphQLResolveInfo, **_kwargs: None
) -> dict[str, dict[str, str | None]]:
    return get_formatted_evidence(parent)
