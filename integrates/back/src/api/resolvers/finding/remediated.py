from db_model.findings.enums import (
    FindingVerificationStatus,
)
from db_model.findings.types import (
    Finding,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)


def resolve(
    parent: Finding, _info: GraphQLResolveInfo, **_kwargs: None
) -> bool:
    return bool(
        parent.verification
        and parent.verification.status == FindingVerificationStatus.REQUESTED
        and not parent.verification.vulnerability_ids
    )
