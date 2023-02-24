from db_model.stakeholders.types import (
    StakeholderPhone,
)
from typing import (
    NamedTuple,
)


class Phone(NamedTuple):
    calling_country_code: str
    national_number: str


def get_international_format_phone_number(
    mobile: Phone | StakeholderPhone,
) -> str:
    return f"+{mobile.calling_country_code}{mobile.national_number}"
