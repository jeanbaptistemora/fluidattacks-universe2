# Standard
from typing import Any

# Third party
from ariadne.utils import convert_kwargs_to_snake_case
from graphql.type.definition import GraphQLResolveInfo

# Local
from backend import util
from backend.decorators import enforce_organization_level_auth_async
from backend.domain import organization as org_domain, user as user_domain
from backend.typing import GrantStakeholderAccessPayload


@convert_kwargs_to_snake_case
@enforce_organization_level_auth_async
async def mutate(
    _parent: None,
    info: GraphQLResolveInfo,
    **parameters: Any
) -> GrantStakeholderAccessPayload:
    success: bool = False

    organization_id = str(parameters.get('organization_id'))
    organization_name = await org_domain.get_name_by_id(organization_id)

    requester_data = await util.get_jwt_content(info.context)
    requester_email = requester_data['user_email']

    user_email = str(parameters.get('user_email'))
    user_phone_number = str(parameters.get('phone_number'))
    user_role = str(parameters.get('role')).lower()

    user_added = await org_domain.add_user(
        organization_id,
        user_email,
        user_role
    )

    user_created = False
    user_exists = bool(await user_domain.get_data(user_email, 'email'))
    if not user_exists:
        user_created = await user_domain.create_without_project(
            user_email,
            'customer',
            user_phone_number
        )
    success = user_added and any([user_created, user_exists])

    if success:
        util.queue_cache_invalidation(
            user_email,
            f'stakeholders*{organization_id.lower()}',
            f'projects*{organization_id.lower()}'
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
