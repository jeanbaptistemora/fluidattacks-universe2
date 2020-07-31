from datetime import datetime
from typing import Dict, List, Union, cast

import pytz
import aioboto3
from django.conf import settings
from backend.dal.helpers import dynamodb
from backend.dal import (
    project as project_dal,
    user as user_dal
)
from backend.domain import organization as org_domain
from backend.typing import User as UserType
from backend.utils.validations import (
    validate_email_address,
    validate_phone_field
)
from backend.utils import (
    aio,
    apm,
)
from backend import authz


async def add_phone_to_user(email: str, phone: str) -> bool:
    """ Update user phone number. """
    return await user_dal.update(email, {'phone': phone})


def get_current_date() -> str:
    tzn = pytz.timezone(settings.TIME_ZONE)  # type: ignore
    today = datetime.now(tz=tzn).today().strftime('%Y-%m-%d %H:%M:%S')
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
    projects = await aio.ensure_io_bound(
        user_dal.get_projects, user_email, active,
    )

    group_level_roles = await aio.ensure_io_bound(
        authz.get_group_level_roles, user_email, projects,
    )

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


def get_group_access(email: str, group: str) -> bool:
    group_level_role = authz.get_group_level_role(email, group)
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


async def update_access_token(email: str, token_data: Dict[str, str]) -> bool:
    """ Update access token """
    access_token = {
        'iat': int(datetime.utcnow().timestamp()),
        'jti': token_data['jti_hashed'],
        'salt': token_data['salt']
    }
    return await user_dal.update(email, {'access_token': access_token})


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


def get(email: str) -> UserType:
    return user_dal.get(email)


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

        org_id = await org_domain.get_or_create('imamura', email)
        if not await org_domain.has_user_access(email, org_id):
            await org_domain.add_user(org_id, email, 'customer')

    return success
