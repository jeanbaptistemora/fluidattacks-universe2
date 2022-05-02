from aioextensions import (
    collect,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from organizations import (
    domain as orgs_domain,
)
from typing import (
    Any,
    cast,
    Dict,
    List,
)


async def resolve(
    parent: Dict[str, Any], _info: GraphQLResolveInfo, **_kwargs: None
) -> List[Dict[str, Any]]:
    user_email = str(parent["user_email"])
    org_ids: List[str] = await orgs_domain.get_user_organizations(user_email)

    return cast(
        List[Dict[str, Any]],
        await collect(tuple(map(orgs_domain.get_by_id, org_ids))),
    )
