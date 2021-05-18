
from graphql.type.definition import GraphQLResolveInfo

from model.findings.types import Finding


def resolve(
    parent: Finding,
    _info: GraphQLResolveInfo,
    **_kwargs: None
) -> str:
    return parent.state.status.value
