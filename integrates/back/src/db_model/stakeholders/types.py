# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from enum import (
    Enum,
)
from typing import (
    NamedTuple,
    Optional,
)


class NotificationsPreferences(NamedTuple):
    email: list[str] = []
    sms: list[str] = []


class StakeholderAccessToken(NamedTuple):
    iat: int
    jti: str
    salt: str


class StateSessionType(str, Enum):
    IS_VALID: str = "IS_VALID"
    REVOKED: str = "REVOKED"


class StakeholderSessionToken(NamedTuple):
    jti: str
    state: StateSessionType


class StakeholderPhone(NamedTuple):
    country_code: str
    calling_country_code: str
    national_number: str


class StakeholderTours(NamedTuple):
    new_group: bool = False
    new_root: bool = False


class Stakeholder(NamedTuple):
    email: str
    access_token: Optional[StakeholderAccessToken] = None
    first_name: Optional[str] = None
    is_concurrent_session: bool = False
    is_registered: bool = False
    last_login_date: Optional[str] = None
    last_name: Optional[str] = None
    legal_remember: bool = False
    notifications_preferences: NotificationsPreferences = (
        NotificationsPreferences()
    )
    phone: Optional[StakeholderPhone] = None
    push_tokens: Optional[list[str]] = None
    registration_date: Optional[str] = None
    role: Optional[str] = None
    tours: StakeholderTours = StakeholderTours()


class StakeholderMetadataToUpdate(NamedTuple):
    access_token: Optional[StakeholderAccessToken] = None
    first_name: Optional[str] = None
    is_concurrent_session: Optional[bool] = None
    is_registered: Optional[bool] = None
    last_login_date: Optional[str] = None
    last_name: Optional[str] = None
    legal_remember: Optional[bool] = None
    notifications_preferences: Optional[NotificationsPreferences] = None
    phone: Optional[StakeholderPhone] = None
    push_tokens: Optional[list[str]] = None
    registration_date: Optional[str] = None
    role: Optional[str] = None
    tours: Optional[StakeholderTours] = None
