# Standard
from typing import cast, Dict, List

# Third party
from aioextensions import collect
from graphql.type.definition import GraphQLResolveInfo

# Local
from backend import util
from backend.domain import organization as org_domain, user as user_domain
from backend.typing import Me, Organization


async def resolve(
    _parent: Me,
    info: GraphQLResolveInfo,
    **_kwargs: None
) -> List[Organization]:
    user_info: Dict[str, str] = await util.get_jwt_content(info.context)
    user_email: str = user_info['user_email']
    org_ids: List[str] = await user_domain.get_organizations(user_email)

    return cast(
        List[Organization],
        await collect(tuple(map(org_domain.get_by_id, org_ids)))
    )
