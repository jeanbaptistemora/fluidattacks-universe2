# Standard
from typing import (
    cast,
    List
)

# Third party
from aioextensions import collect
from ariadne.utils import convert_kwargs_to_snake_case
from graphql.type.definition import GraphQLResolveInfo

# Local
from backend import (
    authz,
    util
)
from backend.decorators import enforce_organization_level_auth_async
from backend.domain import (
    organization as org_domain,
    user as stakeholder_domain
)
from backend.exceptions import (
    InvalidPageIndex,
    InvalidPageSize
)
from backend.typing import (
    GetStakeholdersPayload
    as GetStakeholdersPayloadType,
    Organization as OrganizationType,
    OrganizationStakehodersPageSizeEnum,
    Stakeholder as StakeholderType
)


async def _get_stakeholder(email: str, org_id: str) -> StakeholderType:
    stakeholder: StakeholderType = await stakeholder_domain.get_by_email(email)
    org_role: str = await authz.get_organization_level_role(email, org_id)

    return {**stakeholder, 'responsibility': '', 'role': org_role}


@convert_kwargs_to_snake_case  # type: ignore
@enforce_organization_level_auth_async
async def resolve(
    parent: OrganizationType,
    _info: GraphQLResolveInfo,
    page_index: int,
    page_size: int = 10
) -> GetStakeholdersPayloadType:
    org_id: str = cast(str, parent['id'])
    try:
        OrganizationStakehodersPageSizeEnum(page_size)
    except ValueError:
        raise InvalidPageSize()
    if not page_index >= 1:
        raise InvalidPageIndex()

    items_range = util.get_slice(page_index - 1, int(page_size))

    org_stakeholders: List[str] = await org_domain.get_users(org_id)

    return GetStakeholdersPayloadType(
        stakeholders=await collect(
            _get_stakeholder(email, org_id)
            for email in org_stakeholders[items_range]
        ),
        num_pages=(len(org_stakeholders) // int(page_size)) + 1
    )
