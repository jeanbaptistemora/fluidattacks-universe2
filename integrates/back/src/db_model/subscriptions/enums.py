# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from enum import (
    Enum,
)


class SubscriptionEntity(str, Enum):
    GROUP: str = "GROUP"
    ORGANIZATION: str = "ORGANIZATION"
    PORTFOLIO: str = "PORTFOLIO"


class SubscriptionFrequency(str, Enum):
    DAILY: str = "DAILY"
    HOURLY: str = "HOURLY"
    MONTHLY: str = "MONTHLY"
    NEVER: str = "NEVER"
    WEEKLY: str = "WEEKLY"
