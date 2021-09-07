from db_model.findings.enums import (
    FindingCvssVersion,
)
from db_model.findings.types import (
    Finding,
    Finding31Severity,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)


def resolve(
    parent: Finding, _info: GraphQLResolveInfo, **_kwargs: None
) -> str:
    cvss_version = (
        FindingCvssVersion.V31
        if isinstance(parent.severity, Finding31Severity)
        else FindingCvssVersion.V20
    )
    return cvss_version.value
