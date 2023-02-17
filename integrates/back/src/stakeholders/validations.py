from custom_exceptions import (
    InvalidFieldLength,
    InvalidMobileNumber,
)
from db_model.stakeholders.types import (
    StakeholderPhone,
)
import functools
from newutils import (
    validations,
)
from typing import (
    Any,
    Callable,
)


def validate_phone(phone: StakeholderPhone) -> None:
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


def validate_phone_deco(phone_field: str) -> Callable:
    def wrapper(func: Callable) -> Callable:
        @functools.wraps(func)
        def decorated(*args: Any, **kwargs: Any) -> Any:
            phone = validations.get_attr_value(
                field=phone_field, kwargs=kwargs, obj_type=StakeholderPhone
            )
            validations.check_field_length(
                phone.calling_country_code,
                limit=3,
                is_greater_than_limit=False,
                ex=InvalidMobileNumber(),
            )
            validations.check_field_length(
                phone.calling_country_code,
                limit=0,
                is_greater_than_limit=True,
                ex=InvalidMobileNumber(),
            )
            validations.check_field_length(
                phone.national_number,
                limit=12,
                is_greater_than_limit=False,
                ex=InvalidMobileNumber(),
            )
            validations.check_field_length(
                phone.national_number,
                limit=0,
                is_greater_than_limit=True,
                ex=InvalidMobileNumber(),
            )
            if not (
                phone.calling_country_code.isdecimal()
                and phone.national_number.isdecimal()
            ):
                raise InvalidMobileNumber()
            return func(*args, **kwargs)

        return decorated

    return wrapper
