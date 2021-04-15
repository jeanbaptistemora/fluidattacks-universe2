# Standard Libraries
import re
from typing import (
    cast,
    Dict,
    List,
    Union,
)

# Local libraries
from backend.exceptions import InvalidPushToken
from backend.typing import (
    Invitation as InvitationType,
    User as UserType,
)
from group_access import domain as group_access_domain
from newutils import datetime as datetime_utils
from newutils.validations import (
    validate_alphanumeric_field,
    validate_email_address,
    validate_field_length,
    validate_fluidattacks_staff_on_group,
    validate_phone_field,
)
from users import dal as users_dal


async def acknowledge_concurrent_session(email: str) -> bool:
    """ Acknowledge termination of concurrent session """
    return await users_dal.update(email, {'is_concurrent_session': False})


async def add_phone_to_user(email: str, phone: str) -> bool:
    """ Update user phone number. """
    return await users_dal.update(email, {'phone': phone})


async def add_push_token(user_email: str, push_token: str) -> bool:
    if not re.match(r'^ExponentPushToken\[[a-zA-Z\d_-]+\]$', push_token):
        raise InvalidPushToken()

    user_attrs: dict = await get_attributes(user_email, ['push_tokens'])
    tokens: List[str] = user_attrs.get('push_tokens', [])
    if push_token not in tokens:
        return await users_dal.update(
            user_email,
            {'push_tokens': tokens + [push_token]}
        )
    return True


async def create(email: str, data: UserType) -> bool:
    return await users_dal.create(email, data)


async def delete(email: str) -> bool:
    return await users_dal.delete(email)


async def ensure_user_exists(email: str) -> bool:
    return bool(await users_dal.get(email))


async def get(email: str) -> UserType:
    return await users_dal.get(email)


async def get_attributes(email: str, data: List[str]) -> UserType:
    """ Get attributes of a user. """
    return await users_dal.get_attributes(email, data)


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
    user: UserType = await users_dal.get(email)
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


async def get_user_name(mail: str) -> Dict[str, UserType]:
    return {mail: await get_attributes(mail, ['last_name', 'first_name'])}


async def is_registered(email: str) -> bool:
    return bool(await get_data(email, 'registered'))


async def register(email: str) -> bool:
    return await users_dal.update(email, {'registered': True})


async def remove_push_token(user_email: str, push_token: str) -> bool:
    user_attrs: dict = await get_attributes(user_email, ['push_tokens'])
    tokens: List[str] = list(
        filter(
            lambda token: token != push_token,
            user_attrs.get('push_tokens', [])
        )
    )
    return await users_dal.update(user_email, {'push_tokens': tokens})


async def update(email: str, data_attr: str, name_attr: str) -> bool:
    return await users_dal.update(email, {name_attr: data_attr})


async def update_legal_remember(email: str, remember: bool) -> bool:
    """ Remember legal notice acceptance """
    return await users_dal.update(email, {'legal_remember': remember})


async def update_last_login(email: str) -> bool:
    return await users_dal.update(
        str(email), {'last_login': datetime_utils.get_now_as_str()}
    )


async def update_invited_stakeholder(
    updated_data: Dict[str, str],
    invitation: InvitationType,
    group_name: str
) -> bool:
    success = False
    email = updated_data['email']
    responsibility = updated_data['responsibility']
    phone_number = updated_data['phone_number']
    role = updated_data['role']
    new_invitation = invitation.copy()
    if (
        validate_field_length(responsibility, 50) and
        validate_alphanumeric_field(responsibility) and
        validate_phone_field(phone_number) and
        validate_email_address(email) and
        await validate_fluidattacks_staff_on_group(group_name, email, role)
    ):
        new_invitation['phone_number'] = phone_number
        new_invitation['responsibility'] = responsibility
        new_invitation['role'] = role
        success = await group_access_domain.update(
            email,
            group_name,
            {
                'invitation': new_invitation,

            }
        )
    return success


async def update_multiple_user_attributes(
    email: str,
    data_dict: UserType
) -> bool:
    return await users_dal.update(email, data_dict)
