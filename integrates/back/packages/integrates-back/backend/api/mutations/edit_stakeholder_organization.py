# Standard libraries
from typing import Any

# Third party libraries
from ariadne.utils import convert_kwargs_to_snake_case
from graphql.type.definition import GraphQLResolveInfo

# Local libraries
from backend import util
from backend.dal.helpers.redis import redis_del_by_deps
from backend.decorators import (
    concurrent_decorators,
    enforce_organization_level_auth_async,
    require_login,
    require_organization_access
)
from backend.exceptions import UserNotInOrganization
from backend.typing import EditStakeholderPayload
from organizations import domain as orgs_domain
from users import domain as users_domain


@convert_kwargs_to_snake_case  # type: ignore
@concurrent_decorators(
    require_login,
    require_organization_access,
    enforce_organization_level_auth_async
)
async def mutate(
    _parent: None,
    info: GraphQLResolveInfo,
    **parameters: Any
) -> EditStakeholderPayload:
    success: bool = False

    organization_id: str = str(parameters.get('organization_id'))
    organization_name: str = await orgs_domain.get_name_by_id(organization_id)
    requester_data = await util.get_jwt_content(info.context)
    requester_email = requester_data['user_email']

    user_email: str = str(parameters.get('user_email'))
    new_phone_number: str = str(parameters.get('phone_number'))
    new_role: str = str(parameters.get('role')).lower()

    if not await orgs_domain.has_user_access(organization_id, user_email):
        util.cloudwatch_log(
            info.context,
            f'Security: Stakeholder {requester_email} attempted to edit '
            f'information from a not existent stakeholder {user_email} '
            f'in organization {organization_name}'
        )
        raise UserNotInOrganization()

    if await orgs_domain.add_user(
        organization_id,
        user_email,
        new_role
    ):
        success = await users_domain.edit_user_information(
            info.context,
            {
                'email': user_email,
                'phone_number': new_phone_number,
                'responsibility': ''
            },
            ''
        )

    if success:
        await redis_del_by_deps(
            'edit_stakeholder_organization',
            organization_id=organization_id
        )
        util.cloudwatch_log(
            info.context,
            f'Security: Stakeholder {requester_email} modified '
            f'information from the stakeholder {user_email} '
            f'in the organization {organization_name}'
        )
    else:
        util.cloudwatch_log(
            info.context,
            f'Security: Stakeholder {requester_email} attempted to modify '
            f'information from stakeholder {user_email} in organization '
            f'{organization_name}'
        )
    return EditStakeholderPayload(
        success=success,
        modified_stakeholder=dict(
            email=user_email
        )
    )
