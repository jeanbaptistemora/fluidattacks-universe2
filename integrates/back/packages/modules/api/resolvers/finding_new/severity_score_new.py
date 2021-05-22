from graphql.type.definition import GraphQLResolveInfo

from findings import domain as findings_domain
from model.findings.types import Finding


def resolve(
    parent: Finding, _info: GraphQLResolveInfo, **_kwargs: None
) -> str:
    return findings_domain.get_severity_score_new(parent.severity)
