import re
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from graphql.error import GraphQLError


def validate_email_address(email):
    try:
        validate_email(email)
        return True
    except ValidationError:
        raise GraphQLError('Exception - Email is not valid')


def validate_field(field):
    if field[0].isalnum() or (field[0] == '-' or field[0] is None):
        return True
    raise GraphQLError('Exception - Parameter is not valid')


def validate_phone_field(phone_field):
    if re.match((r'(^\+\d+$)|(^\d+$)|(^$)|(^-$)'), phone_field):
        return True
    raise GraphQLError('Exception - Parameter is not valid')
