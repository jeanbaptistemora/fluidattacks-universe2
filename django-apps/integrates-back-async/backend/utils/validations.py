import re
from operator import methodcaller
from typing import List
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from graphql.error import GraphQLError


def validate_email_address(email: str) -> bool:
    try:
        validate_email(email)
        return True
    except ValidationError:
        raise GraphQLError('Exception - Email is not valid')


def validate_field(field: List[str]) -> bool:
    risk_chars = ['=']
    if not field or field[0] not in risk_chars:
        return True
    raise GraphQLError('Exception - Parameter is not valid')


def validate_alphanumeric_field(field: str) -> bool:
    """Optional whitespace separated string, with alphanumeric characters."""
    if isinstance(field, str):
        return all(map(methodcaller('isalnum'), field.split())) \
            or field == '-' \
            or field == ''

    return field[0] is None


def validate_phone_field(phone_field: str) -> bool:
    if re.match((r'(^\+\d+$)|(^\d+$)|(^$)|(^-$)'), phone_field):
        return True
    raise GraphQLError('Exception - Parameter is not valid')
