import re
from typing import Any
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from graphql.error import GraphQLError


def validate_email_address(email: str) -> bool:
    try:
        validate_email(email)
        return True
    except ValidationError:
        raise GraphQLError('Exception - Email is not valid')


def validate_field(field: Any) -> bool:
    if field[0].isalnum() or (field[0] == '-' or field[0] is None):
        return True
    raise GraphQLError('Exception - Parameter is not valid')


def validate_phone_field(phone_field: str) -> bool:
    if re.match((r'(^\+\d+$)|(^\d+$)|(^$)|(^-$)'), phone_field):
        return True
    raise GraphQLError('Exception - Parameter is not valid')
