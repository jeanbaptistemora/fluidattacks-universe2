# Standard libraries
from typing import Any

# Third party libraries
from ariadne.utils import convert_kwargs_to_snake_case
from graphql.type.definition import GraphQLResolveInfo

# Local libraries
from backend import util
from backend.dal.helpers.redis import redis_del_by_deps
from backend.decorators import enforce_organization_level_auth_async
from backend.typing import GrantStakeholderAccessPayload
from organizations import domain as orgs_domain
from users import domain as users_domain
from users.domain.group import create_without_group


@convert_kwargs_to_snake_case  # type: ignore
@enforce_organization_level_auth_async
async def mutate(
    _parent: None,
    info: GraphQLResolveInfo,
    **parameters: Any
) -> GrantStakeholderAccessPayload:
    success: bool = False

    organization_id = str(parameters.get('organization_id'))
    organization_name = await orgs_domain.get_name_by_id(organization_id)

    requester_data = await util.get_jwt_content(info.context)
    requester_email = requester_data['user_email']

    user_email = str(parameters.get('user_email'))
    user_phone_number = str(parameters.get('phone_number'))
    user_role = str(parameters.get('role')).lower()

    user_added = await orgs_domain.add_user(
        organization_id,
        user_email,
        user_role
    )

    user_created = False
    user_exists = bool(await users_domain.get_data(user_email, 'email'))
    if not user_exists:
        user_created = await create_without_group(
            user_email,
            'customer',
            user_phone_number
        )
    success = user_added and any([user_created, user_exists])

    if success:
        await redis_del_by_deps(
            'grant_stakeholder_organization_access',
            organization_id=organization_id
        )
        util.cloudwatch_log(
            info.context,
            f'Security: Stakeholder {user_email} was granted access '
            f'to organization {organization_name} with role {user_role} '
            f'by stakeholder {requester_email}'
        )
    else:
        util.cloudwatch_log(
            info.context,
            f'Security: Stakeholder {requester_email} attempted to '
            f'grant stakeholder {user_email} {user_role} access to '
            f'organization {organization_name}'
        )

    return GrantStakeholderAccessPayload(
        success=success,
        granted_stakeholder={'email': user_email}
    )
