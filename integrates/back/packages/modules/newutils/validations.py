import re
from typing import List

from backend import authz
from backend.exceptions import (
    InvalidChar,
    InvalidField,
    InvalidFieldLength,
    UnexpectedUserRole,
)

# Constants
FLUIDATTACKS_EMAIL_SUFFIX = '@fluidattacks.com'


async def validate_fluidattacks_staff_on_group(
        group: str,
        email: str,
        role: str) -> bool:
    """Makes sure that Fluid Attacks groups have only Fluid attacks staff."""
    enforcer = await authz.get_group_service_attributes_enforcer(group)

    is_user_at_fluidattacks: bool = email.endswith(FLUIDATTACKS_EMAIL_SUFFIX)
    user_has_hacker_role: bool = (
        role in authz.get_group_level_roles_with_tag('drills', email)
    )

    group_must_only_have_fluidattacks_hackers: bool = enforcer(
        'must_only_have_fluidattacks_hackers'
    )

    if group_must_only_have_fluidattacks_hackers:
        if user_has_hacker_role and not is_user_at_fluidattacks:
            raise UnexpectedUserRole(
                'Groups with any active Fluid Attacks service can '
                'only have Hackers provided by Fluid Attacks'
            )

    return True


def validate_email_address(email: str) -> bool:
    if '+' in email:
        raise InvalidField('email address')
    try:
        check_field(
            email,
            r'^([a-zA-Z0-9_\-\.]+)@([a-zA-Z0-9_\-\.]+)\.([a-zA-Z]{2,5})$'
        )
        return True
    except InvalidChar:
        raise InvalidField('email address')


def validate_fields(fields: List[str]) -> None:
    allowed_chars = (
        r'a-zA-Z0-9ñáéíóúäëïöüÑÁÉÍÓÚÄËÏÖÜ \t\n\r\x0b\x0c(),./:;%@_$#=\?-'
    )
    regex = fr'^[{allowed_chars.replace("=", "")}][{allowed_chars}]*$'
    for field in map(str, fields):
        if field:
            check_field(field, regex)


def validate_url(url: str) -> None:
    clean_url: str = url
    encoded_chars_whitelist: List[str] = ['%20']
    for encoded_char in encoded_chars_whitelist:
        clean_url = clean_url.replace(encoded_char, '')

    if clean_url:
        allowed_chars = r'a-zA-Z0-9(),./:;@_$#=\?-'
        check_field(
            clean_url,
            fr'^[{allowed_chars.replace("=", "")}]+[{allowed_chars}]*$'
        )


def validate_file_name(name: str) -> bool:
    """ Verify that filename has valid characters. """
    name = str(name)
    name_len = len(name.split('.'))
    if name_len <= 2:
        is_valid = bool(re.search(
            '^[A-Za-z0-9!_.*\'()&$@=;:+,? -]*$',
            str(name)
        ))
    else:
        is_valid = False
    return is_valid


def check_field(field: str, regexp: str) -> None:
    if not re.match(regexp, field.strip()):
        raise InvalidChar()


def validate_field_length(
        field: str,
        limit: int,
        is_greater_than_limit: bool = False) -> bool:
    """
    if is_greater_than_limit equals True,
    it means we are checking if field > limit
    """
    if (len(field) > limit) != is_greater_than_limit:
        raise InvalidFieldLength()
    return True


def validate_project_name(project_name: str) -> None:
    if not project_name.isalnum():
        raise InvalidField('project name')


def validate_string_length_between(
    string: str,
    inclusive_lower_bound: int,
    inclusive_upper_bound: int,
) -> None:
    if not inclusive_lower_bound <= len(string) <= inclusive_upper_bound:
        raise InvalidFieldLength()


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
