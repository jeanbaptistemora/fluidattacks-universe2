from graphql.type.definition import GraphQLResolveInfo

from decorators import enforce_group_level_auth_async
from db_model.findings.types import Finding


@enforce_group_level_auth_async
def resolve(
    parent: Finding, _info: GraphQLResolveInfo, **_kwargs: None
) -> str:
    return parent.sorts.value
