from .schema import (
    ORGANIZATION,
)
from db_model.organizations.types import (
    Organization,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from typing import (
    Optional,
)


@ORGANIZATION.field("maxAcceptanceDays")
async def resolve(
    parent: Organization,
    _info: GraphQLResolveInfo,
    **_kwargs: None,
) -> Optional[int]:
    return parent.policies.max_acceptance_days
