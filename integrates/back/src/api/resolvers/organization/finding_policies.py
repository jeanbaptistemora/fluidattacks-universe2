from db_model.organizations.types import (
    Organization,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from organizations_finding_policies.domain import (
    get_org_policies,
)
from organizations_finding_policies.types import (
    OrgFindingPolicy,
)
from typing import (
    Tuple,
)


async def resolve(
    parent: Organization,
    _info: GraphQLResolveInfo,
    **_kwargs: None,
) -> Tuple[OrgFindingPolicy, ...]:
    finding_policies = await get_org_policies(org_name=parent.name)
    return finding_policies
