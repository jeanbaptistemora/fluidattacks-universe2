# Standard
from itertools import chain
from typing import cast, Dict, List

# Third party
from aioextensions import collect
from ariadne.utils import convert_kwargs_to_snake_case
from graphql.type.definition import GraphQLResolveInfo

# Local
from backend import authz, util
from backend.decorators import (
    concurrent_decorators,
    enforce_group_level_auth_async,
    require_integrates
)
from backend.domain import project as group_domain, user as stakeholder_domain
from backend.exceptions import (
    InvalidPageIndex,
    InvalidPageSize
)
from backend.typing import (
    GetStakeholdersPayload
    as GetStakeholdersPayloadType,
    Project as GroupType,
    OrganizationStakehodersPageSizeEnum,
    Stakeholder as StakeholderType,
)
from backend.utils import (
    datetime as datetime_utils,
)


def _filter_by_expired_invitation(
    stakeholders: List[StakeholderType]
) -> List[StakeholderType]:
    return [
        stakeholder
        for stakeholder in stakeholders
        if not (
            stakeholder['invitation_state'] == 'PENDING'
            and stakeholder['invitation_date']
            and datetime_utils.get_plus_delta(
                datetime_utils.get_from_str(
                    cast(str, stakeholder['invitation_date'])
                ),
                weeks=1
            ) < datetime_utils.get_now()
        )
    ]


async def _get_stakeholder(email: str, group_name: str) -> StakeholderType:
    stakeholder: StakeholderType = await stakeholder_domain.get_by_email(email)
    group_role: str = await authz.get_group_level_role(email, group_name)
    access: Dict[str, str] = await group_domain.get_user_access(
        email,
        group_name
    )
    invitation_state = (
        'CONFIRMED' if access.get('has_access', False) else 'PENDING'
    )

    return {
        **stakeholder,
        'responsibility': access.get('responsibility', ''),
        'invitation_date': access.get('invitation_date', ''),
        'invitation_state': invitation_state,
        'role': group_role
    }


@convert_kwargs_to_snake_case  # type: ignore
@concurrent_decorators(
    enforce_group_level_auth_async,
    require_integrates,
)
async def resolve(
    parent: GroupType,
    info: GraphQLResolveInfo,
    page_index: int,
    page_size: int = 10
) -> GetStakeholdersPayloadType:
    group_name: str = cast(str, parent['name'])
    try:
        OrganizationStakehodersPageSizeEnum(page_size)
    except ValueError:
        raise InvalidPageSize()
    if not page_index >= 1:
        raise InvalidPageIndex()

    items_range = util.get_slice(page_index - 1, int(page_size))

    user_data: Dict[str, str] = await util.get_jwt_content(info.context)
    user_email: str = user_data['user_email']

    group_stakeholders_emails = cast(List[str], chain.from_iterable(
        await collect([
            group_domain.get_users(group_name),
            group_domain.get_users(group_name, False)
        ])
    ))
    group_stakeholders_emails = await group_domain.filter_stakeholders(
        group_stakeholders_emails,
        group_name,
        user_email
    )
    group_stakeholders = cast(
        List[StakeholderType],
        await collect(
            _get_stakeholder(email, group_name)
            for email in group_stakeholders_emails
        )
    )

    sorted_group_stakeholders = sorted(
        group_stakeholders,
        key=lambda i: i['invitation_state'],
        reverse=True
    )

    group_stakeholders = _filter_by_expired_invitation(
        sorted_group_stakeholders[items_range]
    )

    return GetStakeholdersPayloadType(
        stakeholders=group_stakeholders,
        num_pages=util.get_num_batches(len(group_stakeholders), int(page_size))
    )
