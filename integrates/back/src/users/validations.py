from custom_exceptions import (
    InvalidFieldLength,
    InvalidMobileNumber,
)
from custom_types import (
    Phone,
)
from newutils import (
    validations,
)


def validate_phone(phone: Phone) -> None:
    try:
        validations.validate_field_length(
            phone.calling_country_code,
            limit=3,
        )
        validations.validate_field_length(
            phone.calling_country_code, limit=0, is_greater_than_limit=True
        )
    except InvalidFieldLength as exc:
        raise InvalidMobileNumber() from exc
    try:
        validations.validate_field_length(
            phone.national_number,
            limit=12,
        )
        validations.validate_field_length(
            phone.national_number, limit=0, is_greater_than_limit=True
        )
    except InvalidFieldLength as exc:
        raise InvalidMobileNumber() from exc

    if not (
        phone.calling_country_code.isdecimal()
        and phone.national_number.isdecimal()
    ):
        raise InvalidMobileNumber()
