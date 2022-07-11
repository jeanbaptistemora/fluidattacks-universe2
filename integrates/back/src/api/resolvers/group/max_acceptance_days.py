from db_model.groups.types import (
    Group,
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


async def resolve(
    parent: Group,
    info: GraphQLResolveInfo,
    **_kwargs: None,
) -> Optional[int]:
    if parent.policies:
        return parent.policies.max_acceptance_days

    organization: Organization = await info.context.loaders.organization.load(
        parent.organization_id
    )
    return organization.policies.max_acceptance_days
