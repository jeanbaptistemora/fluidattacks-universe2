from .schema import (
    FINDING,
)
from db_model.findings.types import (
    Finding,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from newutils.datetime import (
    get_as_str,
)


@FINDING.field("releaseDate")
def resolve(
    parent: Finding, _info: GraphQLResolveInfo, **_kwargs: None
) -> str | None:
    if parent.approval:
        return get_as_str(parent.approval.modified_date)
    return None
