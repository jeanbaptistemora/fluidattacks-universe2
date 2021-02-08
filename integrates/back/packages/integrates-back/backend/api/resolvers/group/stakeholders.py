# Standard libraries
from functools import partial
from itertools import chain
from typing import cast, Dict, List

# Third party libraries
from aioextensions import collect
from graphql.type.definition import GraphQLResolveInfo

# Local libraries
from backend import (
    authz,
    util
)
from backend.dal.helpers.redis import redis_get_or_set_entity_attr
from backend.decorators import (
    concurrent_decorators,
    enforce_group_level_auth_async,
    require_integrates
)
from backend.domain import (
    project as group_domain,
    user as stakeholder_domain
)
from backend.typing import (
    Invitation as InvitationType,
    Project as GroupType,
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
    project_access = await group_domain.get_user_access(
        email,
        group_name
    )
    invitation = cast(InvitationType, project_access.get('invitation'))
    invitation_state = (
        'PENDING' if invitation and not invitation['is_used'] else
        'UNREGISTERED' if not stakeholder.get('is_registered', False) else
        'CONFIRMED'
    )
    if invitation_state == 'PENDING':
        invitation_date = invitation['date']
        responsibility = invitation['responsibility']
        group_role = invitation['role']
        phone_number = invitation['phone_number']
    else:
        invitation_date = ''
        responsibility = cast(str, project_access.get('responsibility', ''))
        group_role = await authz.get_group_level_role(email, group_name)
        phone_number = cast(str, stakeholder['phone_number'])

    return {
        **stakeholder,
        'responsibility': responsibility,
        'invitation_date': invitation_date,
        'invitation_state': invitation_state,
        'phone_number': phone_number,
        'role': group_role
    }


@concurrent_decorators(
    enforce_group_level_auth_async,
    require_integrates,
)
async def resolve(
    parent: GroupType,
    info: GraphQLResolveInfo,
    **kwargs: None
) -> List[StakeholderType]:
    response: List[StakeholderType] = await redis_get_or_set_entity_attr(
        partial(resolve_no_cache, parent, info, **kwargs),
        entity='group',
        attr='stakeholders',
        name=cast(str, parent['name'])
    )

    return response


async def resolve_no_cache(
    parent: GroupType,
    info: GraphQLResolveInfo,
    **_kwargs: None
) -> List[StakeholderType]:
    group_name: str = cast(str, parent['name'])

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
    group_stakeholders = _filter_by_expired_invitation(group_stakeholders)

    return group_stakeholders
