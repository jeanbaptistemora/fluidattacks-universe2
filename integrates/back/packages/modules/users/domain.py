# Standard Libraries
import logging
import logging.config
import re
from datetime import datetime
from typing import (
    Any,
    Awaitable,
    cast,
    Dict,
    List,
    Union
)

# Third libraries
import bugsnag
from aioextensions import collect
from graphql.type.definition import GraphQLResolveInfo

# Local libraries
from back.settings import LOGGING
from backend import (
    authz,
    util,
)
from backend.dal import (
    organization as org_dal,
    user as user_dal,
)
from backend.dal.helpers.redis import redis_del_by_deps_soon
from backend.domain import (
    organization as org_domain,
    project as project_domain,
)
from backend.exceptions import (
    InvalidExpirationTime,
    InvalidPushToken,
)
from backend.typing import (
    Invitation as InvitationType,
    ProjectAccess as ProjectAccessType,
    UpdateAccessTokenPayload as UpdateAccessTokenPayloadType,
    User as UserType,
)
from newutils import (
    apm,
    datetime as datetime_utils,
    groups as groups_utils,
    token as token_helper,
)
from newutils.validations import (
    validate_email_address,
    validate_phone_field,
)
from __init__ import FI_DEFAULT_ORG


logging.config.dictConfig(LOGGING)

# Constants
LOGGER = logging.getLogger(__name__)


async def acknowledge_concurrent_session(email: str) -> bool:
    """ Acknowledge termination of concurrent session """
    return await user_dal.update(email, {'is_concurrent_session': False})


async def add_phone_to_user(email: str, phone: str) -> bool:
    """ Update user phone number. """
    return await user_dal.update(email, {'phone': phone})


async def add_push_token(user_email: str, push_token: str) -> bool:
    if not re.match(r'^ExponentPushToken\[[a-zA-Z\d_-]+\]$', push_token):
        raise InvalidPushToken()

    user_attrs: dict = await get_attributes(user_email, ['push_tokens'])
    tokens: List[str] = user_attrs.get('push_tokens', [])
    if push_token not in tokens:
        return await user_dal.update(
            user_email,
            {'push_tokens': tokens + [push_token]}
        )
    return True


async def complete_register_for_group_invitation(
    project_access: ProjectAccessType
) -> bool:
    coroutines: List[Awaitable[bool]] = []
    success: bool = False
    invitation = cast(InvitationType, project_access['invitation'])
    if invitation['is_used']:
        bugsnag.notify(Exception('Token already used'), severity='warning')

    group_name = cast(str, project_access['project_name'])
    phone_number = cast(str, invitation['phone_number'])
    responsibility = cast(str, invitation['responsibility'])
    role = cast(str, invitation['role'])
    user_email = cast(str, project_access['user_email'])
    updated_invitation = invitation.copy()
    updated_invitation['is_used'] = True

    coroutines.extend([
        project_domain.update_access(
            user_email,
            group_name,
            {
                'expiration_time': None,
                'has_access': True,
                'invitation': updated_invitation,
                'responsibility': responsibility,
            }
        ),
        authz.grant_group_level_role(user_email, group_name, role)
    ])

    organization_id = await org_domain.get_id_for_group(group_name)
    if not await org_domain.has_user_access(organization_id, user_email):
        coroutines.append(
            org_domain.add_user(organization_id, user_email, 'customer')
        )

    if await get_data(user_email, 'email'):
        coroutines.append(add_phone_to_user(user_email, phone_number))
    else:
        coroutines.append(create(user_email, {'phone': phone_number}))

    if not await is_registered(user_email):
        coroutines.extend([
            register(user_email),
            authz.grant_user_level_role(user_email, 'customer')
        ])

    success = all(await collect(coroutines))
    if success:
        redis_del_by_deps_soon(
            'confirm_access',
            group_name=group_name,
            organization_id=organization_id,
        )
    return success


async def create(email: str, data: UserType) -> bool:
    return await user_dal.create(email, data)


async def create_forces_user(
    info: GraphQLResolveInfo,
    group_name: str
) -> bool:
    user_email = format_forces_user_email(group_name)
    success = await groups_utils.invite_to_group(
        email=user_email,
        responsibility='Forces service user',
        role='service_forces',
        phone_number='',
        group_name=group_name
    )

    # Give permissions directly, no confirmation required
    project_access = await project_domain.get_user_access(
        user_email, group_name
    )
    success = (
        success and
        await complete_register_for_group_invitation(project_access)
    )

    if not success:
        LOGGER.error(
            'Couldn\'t grant access to project',
            extra={
                'extra': info.context,
                'username': group_name
            },
        )
    return success


async def create_without_project(
    email: str,
    role: str,
    phone_number: str = ''
) -> bool:
    success = False
    if (
        validate_phone_field(phone_number) and
        validate_email_address(email)
    ):
        new_user_data: UserType = {}
        new_user_data['email'] = email
        new_user_data['authorized'] = True
        new_user_data['registered'] = True
        if phone_number:
            new_user_data['phone'] = phone_number

        success = all(
            await collect([
                authz.grant_user_level_role(email, role),
                create(email, new_user_data)
            ])
        )
        org = await org_domain.get_or_create(FI_DEFAULT_ORG, email)
        if not await org_domain.has_user_access(str(org['id']), email):
            await org_domain.add_user(str(org['id']), email, 'customer')
    return success


async def delete(email: str) -> bool:
    return await user_dal.delete(email)


async def edit_user_information(
    context: Any,
    modified_user_data: Dict[str, str],
    project_name: str
) -> bool:
    coroutines: List[Awaitable[bool]] = []
    email = modified_user_data['email']
    phone = modified_user_data['phone_number']
    responsibility = modified_user_data['responsibility']
    success: bool = False

    if responsibility:
        if len(responsibility) <= 50:
            coroutines.append(
                project_domain.update_access(
                    email,
                    project_name,
                    {'responsibility': responsibility}
                )
            )
        else:
            util.cloudwatch_log(
                context,
                f'Security: {email} Attempted to add responsibility to '
                f'project{project_name} bypassing validation'
            )

    if phone and validate_phone_field(phone):
        coroutines.append(add_phone_to_user(email, phone))
    else:
        util.cloudwatch_log(
            context,
            f'Security: {email} Attempted to edit '
            f'user phone bypassing validation'
        )

    if coroutines:
        success = all(await collect(coroutines))
    return success


async def ensure_user_exists(email: str) -> bool:
    return bool(await user_dal.get(email))


def format_forces_user_email(project_name: str) -> str:
    return f'forces.{project_name}@fluidattacks.com'


async def get(email: str) -> UserType:
    return await user_dal.get(email)


async def get_attributes(email: str, data: List[str]) -> UserType:
    """ Get attributes of a user. """
    return await user_dal.get_attributes(email, data)


async def get_by_email(email: str) -> UserType:
    stakeholder_data: UserType = {
        'email': email,
        'first_login': '',
        'first_name': '',
        'last_login': '',
        'last_name': '',
        'legal_remember': False,
        'phone_number': '-',
        'push_tokens': [],
        'is_registered': True
    }
    user: UserType = await user_dal.get(email)
    if user:
        stakeholder_data.update({
            'email': user['email'],
            'first_login': user.get('date_joined', ''),
            'first_name': user.get('first_name', ''),
            'last_login': user.get('last_login', ''),
            'last_name': user.get('last_name', ''),
            'legal_remember': user.get('legal_remember', False),
            'phone_number': user.get('phone', '-'),
            'push_tokens': user.get('push_tokens', [])
        })
    else:
        stakeholder_data.update({
            'is_registered': False
        })
    return stakeholder_data


async def get_data(email: str, attr: str) -> Union[str, UserType]:
    data_attr = await get_attributes(email, [attr])
    if data_attr and attr in data_attr:
        return cast(UserType, data_attr[attr])
    return str()


async def get_organizations(email: str) -> List[str]:
    return await org_dal.get_ids_for_user(email)


async def get_project_access(email: str, group: str) -> bool:
    group_level_role = await authz.get_group_level_role(email, group)
    return bool(group_level_role)


@apm.trace()
async def get_projects(
    user_email: str,
    active: bool = True,
    organization_id: str = ''
) -> List[str]:
    user_projects: List[str] = []
    projects = await user_dal.get_projects(user_email, active)
    group_level_roles = await authz.get_group_level_roles(user_email, projects)
    can_access_list = await collect(
        project_domain.can_user_access(project, role)
        for role, project in zip(group_level_roles.values(), projects)
    )
    user_projects = [
        project
        for can_access, project in zip(can_access_list, projects)
        if can_access
    ]

    if organization_id:
        org_groups = await org_domain.get_groups(organization_id)
        user_projects = [
            project
            for project in user_projects
            if project in org_groups
        ]
    return user_projects


def is_forces_user(email: str) -> bool:
    """Ensure that is an forces user."""
    pattern = r'forces.(?P<group>\w+)@fluidattacks.com'
    return bool(re.match(pattern, email))


async def is_registered(email: str) -> bool:
    return bool(await get_data(email, 'registered'))


async def register(email: str) -> bool:
    return await user_dal.update(email, {'registered': True})


async def remove_access_token(email: str) -> bool:
    """ Remove access token attribute """
    return await user_dal.update(email, {'access_token': None})


async def remove_push_token(user_email: str, push_token: str) -> bool:
    user_attrs: dict = await get_attributes(user_email, ['push_tokens'])
    tokens: List[str] = list(
        filter(
            lambda token: token != push_token,
            user_attrs.get('push_tokens', [])
        )
    )
    return await user_dal.update(user_email, {'push_tokens': tokens})


async def update(email: str, data_attr: str, name_attr: str) -> bool:
    return await user_dal.update(email, {name_attr: data_attr})


async def update_access_token(
    email: str,
    expiration_time: int,
    **kwargs_token: Any
) -> UpdateAccessTokenPayloadType:
    """ Update access token """
    token_data = util.calculate_hash_token()
    session_jwt = ''
    success = False

    if util.is_valid_expiration_time(expiration_time):
        iat = int(datetime.utcnow().timestamp())
        session_jwt = token_helper.new_encoded_jwt(
            {
                'user_email': email,
                'jti': token_data['jti'],
                'iat': iat,
                'exp': expiration_time,
                'sub': 'api_token',
                **kwargs_token
            },
            api=True
        )
        access_token = {
            'iat': iat,
            'jti': token_data['jti_hashed'],
            'salt': token_data['salt']
        }
        success = await user_dal.update(email, {'access_token': access_token})
    else:
        raise InvalidExpirationTime()

    return UpdateAccessTokenPayloadType(
        success=success,
        session_jwt=session_jwt
    )


async def update_legal_remember(email: str, remember: bool) -> bool:
    """ Remember legal notice acceptance """
    return await user_dal.update(email, {'legal_remember': remember})


async def update_last_login(email: str) -> bool:
    return await user_dal.update(
        str(email), {'last_login': datetime_utils.get_current_date()}
    )


async def update_multiple_user_attributes(
    email: str,
    data_dict: UserType
) -> bool:
    return await user_dal.update(email, data_dict)
