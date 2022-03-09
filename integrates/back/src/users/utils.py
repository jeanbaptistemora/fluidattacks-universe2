from custom_types import (
    Phone,
    StakeholderPhone,
)
from typing import (
    Union,
)


def get_international_format_phone_number(
    mobile: Union[Phone, StakeholderPhone]
) -> str:
    return f"+{mobile.calling_country_code}{mobile.national_number}"
