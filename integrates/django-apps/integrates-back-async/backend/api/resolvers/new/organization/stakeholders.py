# Standard
from typing import cast, List

# Third party
from ariadne.utils import convert_kwargs_to_snake_case
from graphql.type.definition import GraphQLResolveInfo

# Local
from backend.decorators import enforce_organization_level_auth_async
from backend.domain import (
    organization as org_domain,
    user as stakeholder_domain
)
from backend.typing import Organization, Stakeholder
from backend.utils import aio


@convert_kwargs_to_snake_case
@enforce_organization_level_auth_async
async def resolve(
    obj: Organization,
    _info: GraphQLResolveInfo,
    **_kwargs: str
) -> List[Stakeholder]:
    org_id: str = cast(str, obj['id'])

    org_stakeholders: List[str] = await org_domain.get_users(org_id)

    stakeholders: List[Stakeholder] = cast(
        List[Stakeholder],
        await aio.materialize(
            stakeholder_domain.get(email)
            for email in org_stakeholders
        )
    )

    return stakeholders
