from .schema import (
    ORGANIZATION,
)
from db_model.organizations.types import (
    Organization,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)


@ORGANIZATION.field("maxAcceptanceDays")
async def resolve(
    parent: Organization,
    _info: GraphQLResolveInfo,
    **_kwargs: None,
) -> int | None:
    return parent.policies.max_acceptance_days
