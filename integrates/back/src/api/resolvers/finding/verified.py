from .schema import (
    FINDING,
)
from db_model.findings.types import (
    Finding,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from newutils import (
    findings as findings_utils,
)


@FINDING.field("verified")
def resolve(
    parent: Finding, _info: GraphQLResolveInfo, **_kwargs: None
) -> bool:
    return findings_utils.is_verified(
        parent.unreliable_indicators.unreliable_verification_summary
    )
