import re
from typing import List
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from backend.exceptions import InvalidField


def validate_email_address(email: str) -> bool:
    try:
        validate_email(email)
        return True
    except ValidationError:
        raise InvalidField('email address')


def validate_fields(fields: List[str]):
    risk_start_chars = ['=', '?', '<', '`']
    risk_chars = ['\'', '`']
    for field in fields:
        if field and (str(field)[0] in risk_start_chars or
           any(char for char in risk_chars if char in str(field))):
            raise InvalidField()


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
