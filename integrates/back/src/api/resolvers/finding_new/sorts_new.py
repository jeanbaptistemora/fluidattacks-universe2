from db_model.findings.types import (
    Finding,
)
from decorators import (
    enforce_group_level_auth_async,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)


@enforce_group_level_auth_async
def resolve(
    parent: Finding, _info: GraphQLResolveInfo, **_kwargs: None
) -> str:
    return parent.sorts.value
