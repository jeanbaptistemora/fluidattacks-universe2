# Standard
from typing import cast, List

# Third party
from aioextensions import collect
from graphql.type.definition import GraphQLResolveInfo

# Local
from backend.domain import organization as org_domain, user as user_domain
from backend.typing import Me, Organization


async def resolve(
    parent: Me,
    _info: GraphQLResolveInfo,
    **_kwargs: None
) -> List[Organization]:
    user_email: str = cast(str, parent['user_email'])
    org_ids: List[str] = await user_domain.get_organizations(user_email)

    return cast(
        List[Organization],
        await collect(tuple(map(org_domain.get_by_id, org_ids)))
    )
