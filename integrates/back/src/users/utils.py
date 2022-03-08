from custom_types import (
    Phone,
)


def get_international_format_phone_number(mobile: Phone) -> str:
    return f"+{mobile.country_code}{mobile.local_number}"
