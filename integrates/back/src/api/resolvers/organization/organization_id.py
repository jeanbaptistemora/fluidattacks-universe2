from .schema import (
    ORGANIZATION,
)
from db_model.organizations.types import (
    Organization,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)


@ORGANIZATION.field("id")
async def resolve(
    parent: Organization,
    _info: GraphQLResolveInfo,
    **_kwargs: None,
) -> str:
    return parent.id
