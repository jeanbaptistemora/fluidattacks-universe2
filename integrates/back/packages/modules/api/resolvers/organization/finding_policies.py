
from typing import Tuple

from graphql.type.definition import GraphQLResolveInfo

from custom_types import Organization
from organizations_finding_policies.domain import get_org_policies
from organizations_finding_policies.types import OrgFindingPolicy


async def resolve(
    parent: Organization,
    _info: GraphQLResolveInfo,
    **_kwargs: None
) -> Tuple[OrgFindingPolicy, ...]:
    finding_policies: Tuple[OrgFindingPolicy, ...] = await get_org_policies(
        org_name=parent['name']
    )
    return finding_policies
