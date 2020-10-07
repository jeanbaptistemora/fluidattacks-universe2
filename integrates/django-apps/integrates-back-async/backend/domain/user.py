# Standard Libraries
import re
from datetime import datetime
from typing import Any, List, Union, cast, Awaitable

# Third libraries
import json
import aioboto3
from jose import jwt

# Local libraries
from backend.dal.helpers import dynamodb
from backend.dal import (
    organization as org_dal,
    project as project_dal,
    user as user_dal,
)
from backend.domain import organization as org_domain
from backend.exceptions import (
    InvalidPushToken,
    InvalidExpirationTime,
    StakeholderNotFound
)
from backend.typing import (
    User as UserType,
    UpdateAccessTokenPayload as UpdateAccessTokenPayloadType,
)
from backend.utils.validations import (
    validate_email_address,
    validate_phone_field,
)
from backend.utils import (
    aio,
    apm,
    datetime as datetime_utils,
)
from backend import authz
from backend import util

from backend_new import settings


async def add_phone_to_user(email: str, phone: str) -> bool:
    """ Update user phone number. """
    return await user_dal.update(email, {'phone': phone})


def get_current_date() -> str:
    today = datetime_utils.get_as_str(
        datetime_utils.get_now()
    )
    return today


async def get_data(email: str, attr: str) -> Union[str, UserType]:
    data_attr = await get_attributes(email, [attr])
    if data_attr and attr in data_attr:
        return cast(UserType, data_attr[attr])
    return str()


@apm.trace()
async def get_projects(
        user_email: str,
        active: bool = True,
        access_pending_projects: bool = True,
        organization_id: str = '') -> List[str]:
    user_projects: List[str] = []
    projects = await user_dal.get_projects(user_email, active)

    group_level_roles = await authz.get_group_level_roles(user_email, projects)

    async with aioboto3.resource(**dynamodb.RESOURCE_OPTIONS) as resource:
        dynamo_table = await resource.Table(project_dal.TABLE_NAME)
        can_access_list = await aio.materialize(
            project_dal.can_user_access_pending_deletion(
                project, role, access_pending_projects, dynamo_table)
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


async def get_group_access(email: str, group: str) -> bool:
    group_level_role = await authz.get_group_level_role(email, group)
    return bool(group_level_role)


async def get_attributes(email: str, data: List[str]) -> UserType:
    """ Get attributes of a user. """
    return await user_dal.get_attributes(email, data)


async def is_registered(email: str) -> bool:
    return bool(await get_data(email, 'registered'))


async def register(email: str) -> bool:
    return await user_dal.update(email, {'registered': True})


async def remove_access_token(email: str) -> bool:
    """ Remove access token attribute """
    return await user_dal.update(email, {'access_token': None})


async def update_legal_remember(email: str, remember: bool) -> bool:
    """ Remember legal notice acceptance """
    return await user_dal.update(email, {'legal_remember': remember})


async def update_access_token(
        email: str, expiration_time: int,
        **kwargs_token: Any) -> UpdateAccessTokenPayloadType:
    """ Update access token """
    token_data = util.calculate_hash_token()
    session_jwt = ''
    success = False

    if util.is_valid_expiration_time(expiration_time):
        iat = int(datetime.utcnow().timestamp())
        session_jwt = jwt.encode(
            {
                'user_email': email,
                'jti': token_data['jti'],
                'iat': iat,
                'exp': expiration_time,
                'sub': 'api_token',
                **kwargs_token
            },
            algorithm='HS512',
            key=settings.JWT_SECRET_API)
        access_token = {
            'iat': iat,
            'jti': token_data['jti_hashed'],
            'salt': token_data['salt']
        }
        success = await user_dal.update(email, {'access_token': access_token})
    else:
        raise InvalidExpirationTime()

    return UpdateAccessTokenPayloadType(success=success,
                                        session_jwt=session_jwt)


async def update_last_login(email: str) -> bool:
    return await user_dal.update(
        str(email), {'last_login': get_current_date()}
    )


async def update_project_access(
        email: str, project_name: str, access: bool) -> bool:
    return await project_dal.update_access(
        email, project_name, 'has_access', access
    )


async def update_multiple_user_attributes(
        email: str, data_dict: UserType) -> bool:
    return await user_dal.update(email, data_dict)


async def create(email: str, data: UserType) -> bool:
    return await user_dal.create(email, data)


async def update(email: str, data_attr: str, name_attr: str) -> bool:
    return await user_dal.update(email, {name_attr: data_attr})


async def get(email: str) -> UserType:
    return await user_dal.get(email)


async def create_without_project(
    email: str,
    role: str,
    phone_number: str = ''
) -> bool:
    success = False

    if (validate_phone_field(phone_number) and
            validate_email_address(email)):

        new_user_data: UserType = {}
        new_user_data['email'] = email
        new_user_data['authorized'] = True
        new_user_data['registered'] = True
        if phone_number:
            new_user_data['phone'] = phone_number

        success = all(await aio.materialize([
            authz.grant_user_level_role(email, role),
            create(email, new_user_data)
        ]))

        org = await org_domain.get_or_create('okada', email)
        if not await org_domain.has_user_access(str(org['id']), email):
            await org_domain.add_user(str(org['id']), email, 'customer')

    return success


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


async def remove_push_token(user_email: str, push_token: str) -> bool:
    user_attrs: dict = await get_attributes(user_email, ['push_tokens'])
    tokens: List[str] = list(
        filter(
            lambda token: token != push_token,
            user_attrs.get('push_tokens', [])
        )
    )

    return await user_dal.update(user_email, {'push_tokens': tokens})


async def ensure_user_exists(email: str) -> bool:
    return bool(await user_dal.get(email))


def is_forces_user(email: str) -> bool:
    """Ensure that is an forces user."""
    pattern = r'forces.(?P<group>\w+)@fluidattacks.com'
    return bool(re.match(pattern, email))


def format_forces_user_email(project_name: str) -> str:
    return f'forces.{project_name}@fluidattacks.com'


async def get_by_email(email: str) -> UserType:
    user: UserType = await user_dal.get(email)

    if user:
        return {
            'email': user['email'],
            'first_login': user.get('date_joined', ''),
            'first_name': user.get('first_name', ''),
            'last_login': user.get('last_login', ''),
            'last_name': user.get('last_name', ''),
            'legal_remember': user.get('legal_remember', False),
            'phone_number': user.get('phone', '-'),
            'push_tokens': user.get('push_tokens', [])
        }

    raise StakeholderNotFound()


async def get_organizations(email: str) -> List[str]:
    return await org_dal.get_ids_for_user(email)


async def complete_user_register(urltoken: str) -> bool:
    info_json = await util.get_token(f'fi_urltoken:{urltoken}')
    info = json.loads(info_json)

    coroutines: List[Awaitable[bool]] = []
    coroutines.append(
        project_dal.update_access(
            info.get('user_email'),
            info.get('group'),
            'responsibility',
            info.get('responsibility')
        )
    )

    coroutines.append(
        update_project_access(
            info.get('user_email'),
            info.get('group'),
            True
        )
    )

    await util.remove_token(f'fi_urltoken:{urltoken}')

    return all(await aio.materialize(coroutines))
