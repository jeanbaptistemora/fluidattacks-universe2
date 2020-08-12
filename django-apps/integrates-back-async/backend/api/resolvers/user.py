# pylint: disable=too-many-locals
import asyncio
import logging
import sys
import threading
from datetime import datetime
from typing import (
    cast,
    Awaitable,
    Dict,
    List,
    Union,
    Any
)

from ariadne import convert_kwargs_to_snake_case, convert_camel_case_to_snake
from asgiref.sync import sync_to_async

from graphql.type.definition import GraphQLResolveInfo

from backend.api.resolvers import project as project_resolver
from backend.decorators import (
    require_integrates,
    require_login,
    require_organization_access,
    enforce_group_level_auth_async,
    enforce_user_level_auth_async,
)
from backend.domain import (
    organization as org_domain,
    project as project_domain,
    user as user_domain
)
from backend.exceptions import (
    UserNotFound,
)
from backend.typing import (
    User as UserType,
    AddUserPayload as AddUserPayloadType,
    AddStakeholderPayload as AddStakeholderPayloadType,
    GrantUserAccessPayload as GrantUserAccessPayloadType,
    RemoveStakeholderAccessPayload as RemoveStakeholderAccessPayloadType,
    RemoveUserAccessPayload as RemoveUserAccessPayloadType,
    EditUserPayload as EditUserPayloadType,
    EditStakeholderPayload as EditStakeholderPayloadType,
    Project as ProjectType,
)
from backend.services import (
    has_responsibility, has_phone_number,
    has_access_to_project
)
from backend import authz, mailer
from backend.utils import aio
from backend.utils.validations import (
    validate_fluidattacks_staff_on_group,
    validate_email_address, validate_alphanumeric_field, validate_phone_field
)
from backend import util
from fluidintegrates.settings import LOGGING

from __init__ import BASE_URL

logging.config.dictConfig(LOGGING)

# Constants
LOGGER = logging.getLogger(__name__)


async def _give_user_access(
        email: str,
        group: str,
        responsibility: str,
        phone_number: str) -> bool:
    success = False
    coroutines: List[Awaitable[bool]] = []
    coroutines.append(
        project_domain.add_access(
            email, group, 'responsibility', responsibility
        )
    )

    if phone_number and phone_number[1:].isdigit():
        coroutines.append(
            user_domain.add_phone_to_user(email, phone_number)
        )

    coroutines.append(
        user_domain.update_project_access(email, group, True)
    )

    if group and all(await aio.materialize(coroutines)):
        description = await project_domain.get_description(
            group.lower()
        )
        project_url = f'{BASE_URL}/groups/{group.lower()}/indicators'
        mail_to = [email]
        context = {
            'admin': email,
            'project': group,
            'project_description': description,
            'project_url': project_url,
        }
        email_send_thread = threading.Thread(
            name='Access granted email thread',
            target=mailer.send_mail_access_granted,
            args=(mail_to, context,)
        )
        email_send_thread.start()
        success = True
    return success


async def _create_new_user(  # pylint: disable=too-many-arguments
    context: Any,
    email: str,
    responsibility: str,
    role: str,
    phone_number: str,
    group: str,
) -> bool:
    valid = (
        validate_alphanumeric_field(responsibility) and
        validate_phone_field(phone_number) and
        validate_email_address(email) and
        await validate_fluidattacks_staff_on_group(group, email, role)
    )
    success_granted = False
    success_access_given = False
    if valid:
        success_granted = await authz.grant_group_level_role(
            email, group, role
        )

        if not await user_domain.get_data(email, 'email'):
            await user_domain.create(
                email.lower(),
                {
                    'phone': phone_number
                }
            )

        organization_id = await org_domain.get_id_for_group(group)
        if not await org_domain.has_user_access(organization_id, email):
            await org_domain.add_user(organization_id, email, 'customer')

        if not await user_domain.is_registered(email):
            user_domain.register(email)
            await authz.grant_user_level_role(email, 'customer')

        if group and responsibility and len(responsibility) <= 50:
            success_access_given = await _give_user_access(
                email,
                group,
                responsibility,
                phone_number
            )
        else:
            util.cloudwatch_log(
                context,
                (f'Security: {email} Attempted to add responsibility '
                 f'to project {group} without validation')  # pragma: no cover
            )
    return success_granted and success_access_given


@sync_to_async  # type: ignore
def _get_email(_: GraphQLResolveInfo, email: str, *__: str) -> str:
    """Get email."""
    return email.lower()


async def _get_role(
        _: GraphQLResolveInfo,
        email: str,
        entity: str,
        identifier: str) -> str:
    """Get role."""
    if entity == 'PROJECT' and identifier:
        project_name = identifier
        role = await authz.get_group_level_role(email, project_name)
    elif entity == 'ORGANIZATION' and identifier:
        organization_id = identifier
        role = await authz.get_organization_level_role(email, organization_id)
    else:
        role = await authz.get_user_level_role(email)

    return cast(str, role)


async def _get_phone_number(
        _: GraphQLResolveInfo, email: str, *__: str) -> str:
    """Get phone number."""
    return await has_phone_number(email)


async def _get_responsibility(
        _: GraphQLResolveInfo,
        email: str,
        entity: str,
        identifier: str) -> str:
    """Get responsibility."""
    result = ''
    if entity == 'PROJECT':
        project_name = identifier
        result = await has_responsibility(project_name, email)
    return result


async def _get_first_login(_: GraphQLResolveInfo, email: str, *__: str) -> str:
    """Get first login."""
    return cast(str, await user_domain.get_data(email, 'date_joined'))


async def _get_last_login(_: GraphQLResolveInfo, email: str, *__: str) -> str:
    """Get last_login."""
    last_login_response = cast(
        str, await user_domain.get_data(email, 'last_login')
    )
    if last_login_response == '1111-1-1 11:11:11' or not last_login_response:
        last_login = [-1, -1]
    else:
        dates_difference = (
            datetime.now() -
            datetime.strptime(last_login_response, '%Y-%m-%d %H:%M:%S')
        )
        diff_last_login = [dates_difference.days, dates_difference.seconds]
        last_login = diff_last_login
    return str(last_login)


async def _get_projects(
    info: GraphQLResolveInfo,
    email: str,
    *_: str,
    project_as_field: bool = True,
    **__: Any
) -> List[ProjectType]:
    """Get list projects."""
    active_task = asyncio.create_task(user_domain.get_projects(email))
    inactive_task = asyncio.create_task(
        user_domain.get_projects(email, active=False)
    )
    active, inactive = tuple(await asyncio.gather(active_task, inactive_task))
    user_projects = active + inactive
    list_projects = await asyncio.gather(*[
        asyncio.create_task(
            project_resolver.resolve(info, project, as_field=project_as_field)
        )
        for project in user_projects
    ])
    return list_projects


async def resolve(  # pylint: disable=too-many-arguments
    info: GraphQLResolveInfo,
    entity: str,
    email: str,
    identifier: str,
    as_field: bool,
    selection_set: object,
    field_name: str = 'users'
) -> UserType:
    """Async resolve of fields."""
    result = dict()
    requested_fields = (
        util.get_requested_fields(field_name, selection_set)
        if as_field
        else info.field_nodes[0].selection_set.selections
    )

    for requested_field in requested_fields:
        if util.is_skippable(info, requested_field):
            continue
        requested_field = convert_camel_case_to_snake(
            requested_field.name.value
        )
        if requested_field.startswith('_'):
            continue
        resolver_func = getattr(
            sys.modules[__name__],
            f'_get_{requested_field}'
        )
        result[requested_field] = await resolver_func(
            info, email, entity, identifier,
        )
    return result


@enforce_group_level_auth_async
@require_integrates
async def resolve_for_group(  # pylint: disable=too-many-arguments
    info: GraphQLResolveInfo,
    entity: str,
    user_email: str,
    project_name: str = '',
    as_field: bool = False,
    selection_set: object = None,
    field_name: str = 'users'
) -> UserType:
    email = user_email.lower()
    role = await _get_role(info, email, entity, project_name)

    if project_name and role:
        if (not await user_domain.get_data(email, 'email') or
                not await has_access_to_project(email, project_name)):
            raise UserNotFound()

    return await resolve(
        info, entity, email, project_name, as_field, selection_set, field_name
    )


@require_organization_access
async def resolve_for_organization(  # pylint: disable=too-many-arguments
    info: GraphQLResolveInfo,
    entity: str,
    user_email: str,
    organization_id: str = '',
    as_field: bool = False,
    selection_set: object = None
) -> UserType:
    email = user_email.lower()
    return await resolve(
        info, entity, email, organization_id, as_field, selection_set
    )


@convert_kwargs_to_snake_case  # type: ignore
@require_login
async def resolve_user(
    _: Any,
    info: GraphQLResolveInfo,
    entity: str,
    user_email: str,
    **parameters: Any
) -> UserType:
    """Resolve user query."""
    if entity == 'PROJECT':
        project_name = cast(str, parameters.get('project_name'))
        result = await resolve_for_group(
            info, entity, user_email, project_name=project_name
        )
    elif entity == 'ORGANIZATION':
        organization_id = cast(str, parameters.get('organization_id'))
        result = await resolve_for_organization(
            info, entity, user_email, organization_id=organization_id
        )
    return result


@convert_kwargs_to_snake_case  # type: ignore
async def resolve_user_mutation(
    obj: Any,
    info: GraphQLResolveInfo,
    **parameters: Any
) -> Union[
    AddUserPayloadType,
    GrantUserAccessPayloadType,
    RemoveUserAccessPayloadType,
    EditUserPayloadType
]:
    """Wrap user mutations."""
    field = util.camelcase_to_snakecase(info.field_name)
    resolver_func = getattr(sys.modules[__name__], f'_do_{field}')
    return cast(
        Union[
            AddUserPayloadType,
            GrantUserAccessPayloadType,
            RemoveUserAccessPayloadType,
            EditUserPayloadType
        ],
        await resolver_func(obj, info, **parameters)
    )


@require_login
@enforce_user_level_auth_async
async def _do_add_user(
    _: Any,
    info: GraphQLResolveInfo,
    email: str,
    role: str,
    phone_number: str = ''
) -> AddUserPayloadType:
    """Resolve add_user mutation."""
    success: bool = False

    user_data = util.get_jwt_content(info.context)
    user_email = user_data['user_email']

    allowed_roles_to_grant = await authz.get_user_level_roles_a_user_can_grant(
        requester_email=user_email,
    )

    if role in allowed_roles_to_grant:
        new_user = await user_domain.create_without_project(
            email=email,
            role=role,
            phone_number=phone_number,
        )
        if new_user:
            util.cloudwatch_log(
                info.context,
                f'Security: Add user {email}')  # pragma: no cover
            mail_to = [email]
            context = {'admin': email}
            email_send_thread = threading.Thread(
                name='Access granted email thread',
                target=mailer.send_mail_access_granted,
                args=(mail_to, context,)
            )
            email_send_thread.start()
            success = True
        else:
            LOGGER.error(
                'Error: Couldn\'t grant user access',
                extra={'extra': info.context})
    else:
        LOGGER.error(
            'Invalid role provided',
            extra={
                'extra': {
                    'email': email,
                    'requester_email': user_email,
                    'role': role
                }
            })

    return AddUserPayloadType(success=success, email=email)


@require_login
@enforce_user_level_auth_async
async def _do_add_stakeholder(
    _: Any,
    info: GraphQLResolveInfo,
    email: str,
    role: str,
    phone_number: str = ''
) -> AddStakeholderPayloadType:
    success: bool = False

    user_data = util.get_jwt_content(info.context)
    user_email = user_data['user_email']

    allowed_roles_to_grant = await authz.get_user_level_roles_a_user_can_grant(
        requester_email=user_email,
    )

    if role in allowed_roles_to_grant:
        new_user = await user_domain.create_without_project(
            email=email,
            role=role,
            phone_number=phone_number,
        )
        if new_user:
            util.cloudwatch_log(
                info.context,
                f'Security: Add stakeholder {email}'
            )
            mail_to = [email]
            context = {'admin': email}
            email_send_thread = threading.Thread(
                name='Access granted email thread',
                target=mailer.send_mail_access_granted,
                args=(mail_to, context,)
            )
            email_send_thread.start()
            success = True
        else:
            LOGGER.error(
                'Error: Couldn\'t grant stakeholder access',
                extra={'extra': info.context})
    else:
        LOGGER.error(
            'Invalid role provided',
            extra={
                'extra': {
                    'email': email,
                    'requester_email': user_email,
                    'role': role
                }
            })

    return AddStakeholderPayloadType(success=success, email=email)


@require_login
@enforce_group_level_auth_async
@require_integrates
async def _do_grant_user_access(
        _: Any,
        info: GraphQLResolveInfo,
        role: str,
        **query_args: str) -> GrantUserAccessPayloadType:
    """Resolve grant_user_access mutation."""
    project_name = query_args.get('project_name', '').lower()
    success = False
    user_data = util.get_jwt_content(info.context)
    user_email = user_data['user_email']

    new_user_role = role
    new_user_email = query_args.get('email', '')

    allowed_roles_to_grant = \
        await authz.get_group_level_roles_a_user_can_grant(
            group=project_name,
            requester_email=user_email,
        )

    if new_user_role in allowed_roles_to_grant:
        if await _create_new_user(
                context=info.context,
                email=new_user_email,
                responsibility=query_args.get('responsibility', '-'),
                role=new_user_role,
                phone_number=query_args.get('phone_number', ''),
                group=project_name):
            success = True
        else:
            LOGGER.error(
                'Couldn\'t grant access to project',
                extra={'extra': info.context})
    else:
        LOGGER.error(
            'Invalid role provided',
            extra={
                'extra': {
                    'new_user_role': new_user_role,
                    'project_name': project_name,
                    'requester_email': user_email
                }
            })

    if success:
        await util.invalidate_cache(project_name, new_user_email)
        util.cloudwatch_log(
            info.context,
            (f'Security: Given grant access to {new_user_email} '
             f'in {project_name} project')  # pragma: no cover
        )
    else:
        util.cloudwatch_log(
            info.context,
            (f'Security: Attempted to grant access to {new_user_email} '
             f'in {project_name} project')  # pragma: no cover
        )

    return GrantUserAccessPayloadType(
        success=success,
        granted_user=dict(
            project_name=project_name,
            email=new_user_email
        )
    )


@require_login
@enforce_group_level_auth_async
@require_integrates
async def _do_remove_user_access(
        _: Any,
        info: GraphQLResolveInfo,
        project_name: str,
        user_email: str) -> RemoveUserAccessPayloadType:
    """Resolve remove_user_access mutation."""
    success = await project_domain.remove_user_access(
        project_name, user_email
    )
    removed_email = user_email if success else ''
    if success:
        await util.invalidate_cache(project_name, user_email)
        util.cloudwatch_log(
            info.context,
            (f'Security: Removed user: {user_email} from {project_name} '
             'project successfully')  # pragma: no cover
        )
    else:
        util.cloudwatch_log(
            info.context,
            (f'Security: Attempted to remove user: {user_email} '
             f'from {project_name} project')  # pragma: no cover
        )
    return RemoveUserAccessPayloadType(
        success=success,
        removed_email=removed_email
    )


@require_login
@enforce_group_level_auth_async
@require_integrates
async def _do_remove_stakeholder_access(
        _: Any,
        info: GraphQLResolveInfo,
        project_name: str,
        user_email: str) -> RemoveStakeholderAccessPayloadType:
    success = await project_domain.remove_user_access(
        project_name, user_email
    )
    removed_email = user_email if success else ''
    if success:
        await util.invalidate_cache(project_name, user_email)
        msg = (
            f'Security: Removed stakeholder: {user_email} from {project_name} '
            f'project successfully'
        )
        util.cloudwatch_log(info.context, msg)
    else:
        msg = (
            f'Security: Attempted to remove stakeholder: {user_email} '
            f'from {project_name} project'
        )
        util.cloudwatch_log(info.context, msg)
    return RemoveStakeholderAccessPayloadType(
        success=success,
        removed_email=removed_email
    )


@require_login
@enforce_group_level_auth_async
@require_integrates
async def _do_edit_user(
        _: Any,
        info: GraphQLResolveInfo,
        **modified_user_data: str) -> EditUserPayloadType:
    """Resolve edit_user mutation."""
    project_name = modified_user_data['project_name'].lower()
    modified_role = modified_user_data['role']
    modified_email = modified_user_data['email']

    success = False
    user_data = util.get_jwt_content(info.context)
    user_email = user_data['user_email']

    allowed_roles_to_grant = \
        await authz.get_group_level_roles_a_user_can_grant(
            group=project_name,
            requester_email=user_email,
        )

    await validate_fluidattacks_staff_on_group(
        project_name, modified_email, modified_role
    )

    if modified_role in allowed_roles_to_grant:
        if await authz.grant_group_level_role(
                modified_email, project_name, modified_role):
            success = await modify_user_information(
                info.context, modified_user_data, project_name
            )
        else:
            LOGGER.error(
                'Couldn\'t update user role',
                extra={'extra': info.context})
    else:
        LOGGER.error(
            'Invalid role provided',
            extra={
                'extra': {
                    'modified_user_role': modified_role,
                    'project_name': project_name,
                    'requester_email': user_email
                }
            })

    if success:
        await util.invalidate_cache(project_name, modified_email)
        util.cloudwatch_log(
            info.context,
            (f'Security: Modified user data:{modified_email} '
             'in {project_name} project successfully')  # pragma: no cover
        )
    else:
        util.cloudwatch_log(
            info.context,
            ('Security: Attempted to modify user '
             f'data:{modified_email} in '
             f'{project_name} project')  # pragma: no cover
        )

    return EditUserPayloadType(
        success=success,
        modified_user=dict(
            project_name=project_name,
            email=modified_user_data['email']
        )
    )


@require_login
@enforce_group_level_auth_async
@require_integrates
async def _do_edit_stakeholder(
        _: Any,
        info: GraphQLResolveInfo,
        **modified_user_data: str) -> EditStakeholderPayloadType:
    project_name = modified_user_data['project_name'].lower()
    modified_role = modified_user_data['role']
    modified_email = modified_user_data['email']

    success = False
    user_data = util.get_jwt_content(info.context)
    user_email = user_data['user_email']

    allowed_roles_to_grant = \
        await authz.get_group_level_roles_a_user_can_grant(
            group=project_name,
            requester_email=user_email,
        )

    await validate_fluidattacks_staff_on_group(
        project_name, modified_email, modified_role
    )

    if modified_role in allowed_roles_to_grant:
        if await authz.grant_group_level_role(
                modified_email, project_name, modified_role):
            success = await modify_user_information(
                info.context, modified_user_data, project_name
            )
        else:
            LOGGER.error(
                'Couldn\'t update stakeholder role',
                extra={'extra': info.context})
    else:
        LOGGER.error(
            'Invalid role provided',
            extra={
                'extra': {
                    'modified_user_role': modified_role,
                    'project_name': project_name,
                    'requester_email': user_email
                }
            })

    if success:
        await util.invalidate_cache(project_name, modified_email)
        msg = (
            f'Security: Modified stakeholder data: {modified_email} '
            f'in {project_name} project successfully'
        )
        util.cloudwatch_log(info.context, msg)
    else:
        msg = (
            f'Security: Attempted to modify stakeholder '
            f'data:{modified_email} in '
            f'{project_name} project'
        )
        util.cloudwatch_log(info.context, msg)

    return EditStakeholderPayloadType(
        success=success,
        modified_user=dict(
            project_name=project_name,
            email=modified_user_data['email']
        )
    )


async def _add_acess(
        responsibility: str,
        email: str,
        project_name: str,
        context: object) -> bool:
    result = False
    if len(responsibility) <= 50:
        result = await project_domain.add_access(
            email, project_name, 'responsibility', responsibility
        )
    else:
        util.cloudwatch_log(
            context,
            (f'Security: {email} Attempted to add responsibility to '
             f'project{project_name} bypassing validation')
        )
    return result


async def modify_user_information(
        context: Any,
        modified_user_data: Dict[str, str],
        project_name: str) -> bool:
    """Modify user information."""
    email = modified_user_data['email']
    responsibility = modified_user_data['responsibility']
    phone = modified_user_data['phone_number']
    coroutines: List[Awaitable[bool]] = []

    if responsibility:
        coroutines.append(_add_acess(
            responsibility,
            email,
            project_name,
            context
        ))

    if phone and validate_phone_field(phone):
        coroutines.append(
            user_domain.add_phone_to_user(email, phone)
        )
    else:
        util.cloudwatch_log(
            context,
            (f'Security: {email} Attempted to edit user '
             'phone bypassing validation')
        )
        return False

    return all(await aio.materialize(coroutines))


@convert_kwargs_to_snake_case  # type: ignore
@require_login
@enforce_user_level_auth_async
async def resolve_user_list_projects(
        _: Any,
        info: GraphQLResolveInfo,
        user_email: str) -> List[ProjectType]:
    """Resolve user_list_projects query."""
    email: str = await _get_email(info, user_email)

    return await _get_projects(info, email, project_as_field=False)
