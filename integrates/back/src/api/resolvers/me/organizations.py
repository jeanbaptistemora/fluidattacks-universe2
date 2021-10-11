from aioextensions import (
    collect,
)
from custom_types import (
    Me,
    Organization,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from organizations import (
    domain as orgs_domain,
)
from typing import (
    cast,
    List,
)


async def resolve(
    parent: Me, _info: GraphQLResolveInfo, **_kwargs: None
) -> List[Organization]:
    user_email: str = parent["user_email"]
    org_ids: List[str] = await orgs_domain.get_user_organizations(user_email)

    return cast(
        List[Organization],
        await collect(tuple(map(orgs_domain.get_by_id, org_ids))),
    )
