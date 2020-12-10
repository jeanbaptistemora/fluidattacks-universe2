# pylint: disable=too-many-locals
import logging
import sys
from typing import (
    cast,
    Awaitable,
    Dict,
    List,
    Union,
    Any
)

from aioextensions import (
    collect,
    schedule,
)
from ariadne import convert_kwargs_to_snake_case

from graphql.type.definition import GraphQLResolveInfo

from backend.decorators import (
    concurrent_decorators,
    require_integrates,
    require_login,
    enforce_group_level_auth_async,
)
from backend.domain import (
    organization as org_domain,
    project as project_domain,
    user as user_domain
)
from backend.typing import (
    AddStakeholderPayload as AddStakeholderPayloadType,
    GrantStakeholderAccessPayload as GrantStakeholderAccessPayloadType,
    RemoveStakeholderAccessPayload as RemoveStakeholderAccessPayloadType,
    EditStakeholderPayload as EditStakeholderPayloadType,
    MailContent as MailContentType,
)
from backend import authz, mailer
from backend.utils.validations import (
    validate_fluidattacks_staff_on_group,
    validate_email_address, validate_alphanumeric_field, validate_phone_field
)
from backend import util
from backend_new.settings import LOGGING

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

    if phone_number and phone_number[1:].isdigit():
        coroutines.append(
            user_domain.add_phone_to_user(email, phone_number)
        )

    if group and all(await collect(coroutines)):
        urltoken = await util.create_confirm_access_token(
            email, group, responsibility
        )
        description = await project_domain.get_description(
            group.lower()
        )
        project_url = f'{BASE_URL}/confirm_access/{urltoken}'
        mail_to = [email]
        context: MailContentType = {
            'admin': email,
            'project': group,
            'project_description': description,
            'project_url': project_url,
        }
        schedule(
            mailer.send_mail_access_granted(
                mail_to, context,
            )
        )
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
            await collect((
                user_domain.register(email),
                authz.grant_user_level_role(email, 'customer')
            ))

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


@convert_kwargs_to_snake_case  # type: ignore
async def resolve_user_mutation(
    obj: Any,
    info: GraphQLResolveInfo,
    **parameters: Any
) -> Union[
    AddStakeholderPayloadType,
    GrantStakeholderAccessPayloadType,
    RemoveStakeholderAccessPayloadType,
    EditStakeholderPayloadType
]:
    """Wrap user mutations."""
    field = util.camelcase_to_snakecase(info.field_name)
    resolver_func = getattr(sys.modules[__name__], f'_do_{field}')
    return cast(
        Union[
            AddStakeholderPayloadType,
            GrantStakeholderAccessPayloadType,
            RemoveStakeholderAccessPayloadType,
            EditStakeholderPayloadType
        ],
        await resolver_func(obj, info, **parameters)
    )


@concurrent_decorators(
    require_login,
    enforce_group_level_auth_async,
    require_integrates,
)
async def _do_grant_stakeholder_access(
        _: Any,
        info: GraphQLResolveInfo,
        role: str,
        **query_args: str) -> GrantStakeholderAccessPayloadType:
    project_name = query_args.get('project_name', '').lower()
    success = False
    user_data = await util.get_jwt_content(info.context)
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
        util.queue_cache_invalidation(
            f'stakeholders*{project_name}',
            new_user_email
        )
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

    return GrantStakeholderAccessPayloadType(
        success=success,
        granted_stakeholder=dict(
            project_name=project_name,
            email=new_user_email
        )
    )


@concurrent_decorators(
    require_login,
    enforce_group_level_auth_async,
    require_integrates,
)
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
        util.queue_cache_invalidation(
            f'stakeholders*{project_name}',
            user_email
        )
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


@concurrent_decorators(
    require_login,
    enforce_group_level_auth_async,
    require_integrates,
)
async def _do_edit_stakeholder(
        _: Any,
        info: GraphQLResolveInfo,
        **modified_user_data: str) -> EditStakeholderPayloadType:
    project_name = modified_user_data['project_name'].lower()
    modified_role = modified_user_data['role']
    modified_email = modified_user_data['email']

    success = False
    user_data = await util.get_jwt_content(info.context)
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
        util.queue_cache_invalidation(
            f'stakeholders*{project_name}',
            modified_email
        )
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
        modified_stakeholder=dict(
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

    return all(await collect(coroutines))
