# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from db_model.stakeholders.types import (
    StakeholderPhone,
)
from typing import (
    NamedTuple,
    Union,
)


class Phone(NamedTuple):
    calling_country_code: str
    national_number: str


def get_international_format_phone_number(
    mobile: Union[Phone, StakeholderPhone]
) -> str:
    return f"+{mobile.calling_country_code}{mobile.national_number}"
