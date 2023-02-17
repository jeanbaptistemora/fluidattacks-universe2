from .schema import (
    FINDING,
)
from db_model.findings.types import (
    Finding,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from typing import (
    Dict,
)


@FINDING.field("verificationSummary")
def resolve(
    parent: Finding, _info: GraphQLResolveInfo, **_kwargs: None
) -> Dict[str, int]:
    return (
        parent.unreliable_indicators.unreliable_verification_summary._asdict()
    )
