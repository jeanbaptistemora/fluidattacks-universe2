import re
from typing import List
from django.core.exceptions import ValidationError
from django.core.validators import validate_email

from backend import authz
from backend.exceptions import (
    InvalidChar,
    InvalidField,
    InvalidFieldLength,
    UnexpectedUserRole,
)

# Constants
FLUIDATTACKS_EMAIL_SUFFIX = '@fluidattacks.com'


async def validate_fluidattacks_staff_on_group(group, email, role) -> bool:
    """Makes sure that Fluid Attacks groups have only Fluid attacks staff."""
    enforcer = authz.get_group_service_attributes_enforcer(group)

    is_user_at_fluidattacks: bool = email.endswith(FLUIDATTACKS_EMAIL_SUFFIX)
    user_has_hacker_role: bool = \
        role in authz.get_group_level_roles_with_tag('drills')

    group_must_only_have_fluidattacks_hackers: bool = \
        await enforcer(group, 'must_only_have_fluidattacks_hackers')

    if group_must_only_have_fluidattacks_hackers:
        if user_has_hacker_role and not is_user_at_fluidattacks:
            raise UnexpectedUserRole('Groups with any active Fluid Attacks service can '
                                     'only have Hackers provided by Fluid Attacks')

    group_is_fluidattacks_customer: bool = \
        await enforcer(group, 'is_fluidattacks_customer')

    if not group_is_fluidattacks_customer and is_user_at_fluidattacks:
        raise UnexpectedUserRole('Groups without an active Fluid Attacks service can '
                                 'not have Fluid Attacks staff')

    return True


def validate_email_address(email: str) -> bool:
    if '+' in email:
        raise InvalidField('email address')
    try:
        validate_email(email)
        return True
    except ValidationError:
        raise InvalidField('email address')


def validate_fields(fields: List[str]):
    whitelist: str = (
        '0123456789'
        'abcdefghijklmnopqrstuvwxyzñáéíóúäëïöü'
        'ABCDEFGHIJKLMNOPQRSTUVWXYZÑÁÉÍÓÚÄËÏÖÜ'
        ' \t\n\r\x0b\x0c'
        '(),-./:;@_'
    )

    for field in map(str, fields):
        for char in field:
            if char not in whitelist:
                raise InvalidChar()


def validate_field_length(field: str, limit: int):
    if len(field) >= limit:
        raise InvalidFieldLength()


def validate_project_name(project_name: str):
    if not project_name.isalnum():
        raise InvalidField('project name')


def validate_alphanumeric_field(field: str) -> bool:
    """Optional whitespace separated string, with alphanumeric characters."""
    is_alnum = all([word.isalnum() for word in field.split()])
    if is_alnum or field == '-' or not field:
        return True
    raise InvalidField()


def validate_phone_field(phone_field: str) -> bool:
    if re.match((r'(^\+\d+$)|(^\d+$)|(^$)|(^-$)'), phone_field):
        return True
    raise InvalidField('phone number')
