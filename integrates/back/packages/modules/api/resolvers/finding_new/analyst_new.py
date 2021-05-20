
from graphql.type.definition import GraphQLResolveInfo

from decorators import enforce_group_level_auth_async
from model.findings.types import Finding


@enforce_group_level_auth_async
def resolve(
    parent: Finding,
    _info: GraphQLResolveInfo,
    **_kwargs: None
) -> str:
    return parent.analyst_email
