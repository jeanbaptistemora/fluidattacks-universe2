from .schema import (
    FINDING,
)
from db_model.findings.types import (
    Finding,
)
from db_model.vulnerabilities.utils import (
    get_current_state_converted,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)


@FINDING.field("state")
def resolve(
    parent: Finding, _info: GraphQLResolveInfo, **_kwargs: None
) -> str:
    return get_current_state_converted(
        parent.unreliable_indicators.unreliable_status.value.upper()
    ).lower()
