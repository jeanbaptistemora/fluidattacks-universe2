import sys
from typing import (
    Any,
)

from ariadne import (
    convert_kwargs_to_snake_case
)
from graphql.type.definition import GraphQLResolveInfo

from backend import util
from backend.api.resolvers import (
    user as user_loader,
)
from backend.decorators import (
    concurrent_decorators,
    enforce_organization_level_auth_async,
    require_login,
    require_organization_access
)
from backend.domain import (
    organization as org_domain,
    user as user_domain
)
from backend.exceptions import (
    UserNotInOrganization
)
from backend.typing import (
    EditStakeholderPayload as EditStakeholderPayloadType,
    GrantStakeholderAccessPayload as GrantStakeholderAccessPayloadType,
    SimplePayload as SimplePayloadType,
)


@concurrent_decorators(
    require_organization_access,
    enforce_organization_level_auth_async,
)
async def _do_edit_stakeholder_organization(
    _: Any,
    info: GraphQLResolveInfo,
    **parameters: Any
) -> EditStakeholderPayloadType:
    success: bool = False

    organization_id: str = str(parameters.get('organization_id'))
    organization_name: str = await org_domain.get_name_by_id(organization_id)
    requester_data = await util.get_jwt_content(info.context)
    requester_email = requester_data['user_email']

    user_email: str = str(parameters.get('user_email'))
    new_phone_number: str = str(parameters.get('phone_number'))
    new_role: str = str(parameters.get('role')).lower()

    if not await org_domain.has_user_access(organization_id, user_email):
        util.cloudwatch_log(
            info.context,
            f'Security: Stakeholder {requester_email} attempted to edit '
            f'information from a not existent stakeholder {user_email} '
            f'in organization {organization_name}'
        )
        raise UserNotInOrganization()

    if await org_domain.add_user(
        organization_id,
        user_email,
        new_role
    ):
        success = await user_loader.modify_user_information(
            info.context,
            {
                'email': user_email,
                'phone_number': new_phone_number,
                'responsibility': ''
            },
            ''
        )

    if success:
        util.queue_cache_invalidation(
            user_email,
            f'stakeholders*{organization_id.lower()}',
            f'projects*{organization_id.lower()}'
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
    return EditStakeholderPayloadType(
        success=success,
        modified_stakeholder=dict(
            email=user_email
        )
    )


@concurrent_decorators(
    require_organization_access,
    enforce_organization_level_auth_async,
)
async def _do_grant_stakeholder_organization_access(
    _: Any,
    info: GraphQLResolveInfo,
    **parameters: Any
) -> GrantStakeholderAccessPayloadType:
    success: bool = False

    organization_id = str(parameters.get('organization_id'))
    organization_name = await org_domain.get_name_by_id(organization_id)

    requester_data = await util.get_jwt_content(info.context)
    requester_email = requester_data['user_email']

    user_email = str(parameters.get('user_email'))
    user_phone_number = str(parameters.get('phone_number'))
    user_role = str(parameters.get('role')).lower()

    user_added = await org_domain.add_user(
        organization_id, user_email, user_role
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

    return GrantStakeholderAccessPayloadType(
        success=success,
        granted_stakeholder=dict(
            email=user_email
        )
    )


@concurrent_decorators(
    require_organization_access,
    enforce_organization_level_auth_async,
)
async def _do_remove_stakeholder_organization_access(
    _: Any,
    info: GraphQLResolveInfo,
    organization_id: str,
    user_email: str
) -> SimplePayloadType:
    user_data = await util.get_jwt_content(info.context)
    requester_email = user_data['user_email']
    organization_name = await org_domain.get_name_by_id(organization_id)

    success: bool = await org_domain.remove_user(
        organization_id, user_email.lower()
    )
    if success:
        util.queue_cache_invalidation(
            user_email,
            f'stakeholders*{organization_id.lower()}',
        )
        util.cloudwatch_log(
            info.context,
            f'Security: Stakeholder {requester_email} removed stakeholder'
            f' {user_email} from organization {organization_name}'
        )
    else:
        util.cloudwatch_log(
            info.context,
            f'Security: Stakeholder {requester_email} attempted to remove '
            f'stakeholder {user_email} from organization {organization_name}'
        )

    return SimplePayloadType(success=success)


@concurrent_decorators(
    require_organization_access,
    enforce_organization_level_auth_async,
)
async def _do_update_organization_policies(
    _: Any,
    info: GraphQLResolveInfo,
    **parameters: Any
) -> SimplePayloadType:
    user_data = await util.get_jwt_content(info.context)
    user_email = user_data['user_email']

    organization_id = parameters.pop('organization_id')
    organization_name = parameters.pop('organization_name')
    success: bool = await org_domain.update_policies(
        organization_id,
        organization_name,
        user_email,
        parameters
    )
    if success:
        util.cloudwatch_log(
            info.context,
            f'Security: User {user_email} updated policies for organization '
            f'{organization_name} with ID {organization_id}'
        )
    return SimplePayloadType(success=success)


@convert_kwargs_to_snake_case  # type: ignore
@require_login
async def resolve_organization_mutation(
        obj: Any,
        info: GraphQLResolveInfo,
        **parameters: Any) -> Any:
    """Resolve Organization mutation """
    field = util.camelcase_to_snakecase(info.field_name)
    resolver_func = getattr(sys.modules[__name__], f'_do_{field}')
    return await resolver_func(obj, info, **parameters)
