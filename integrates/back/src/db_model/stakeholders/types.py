from datetime import (
    datetime,
)
from decimal import (
    Decimal,
)
from enum import (
    Enum,
)
from typing import (
    NamedTuple,
)


class NotificationsParameters(NamedTuple):
    min_severity: Decimal = Decimal("3.0")


class NotificationsPreferences(NamedTuple):
    available: list[str] = []
    email: list[str] = []
    sms: list[str] = []
    parameters: NotificationsParameters = NotificationsParameters()


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
    new_risk_exposure: bool = True
    welcome: bool = False


class StakeholderState(NamedTuple):
    modified_by: str | None
    modified_date: datetime | None
    notifications_preferences: NotificationsPreferences = (
        NotificationsPreferences()
    )


class Stakeholder(NamedTuple):
    email: str
    access_token: StakeholderAccessToken | None = None
    enrolled: bool = False
    first_name: str | None = None
    is_concurrent_session: bool = False
    is_registered: bool = False
    last_login_date: datetime | None = None
    last_api_token_use_date: datetime | None = None
    last_name: str | None = None
    legal_remember: bool = False
    phone: StakeholderPhone | None = None
    registration_date: datetime | None = None
    role: str | None = None
    session_key: str | None = None
    session_token: StakeholderSessionToken | None = None
    state: StakeholderState = StakeholderState(
        notifications_preferences=NotificationsPreferences(),
        modified_by=None,
        modified_date=None,
    )
    tours: StakeholderTours = StakeholderTours()


class StakeholderMetadataToUpdate(NamedTuple):
    access_token: StakeholderAccessToken | None = None
    enrolled: bool | None = None
    first_name: str | None = None
    is_concurrent_session: bool | None = None
    is_registered: bool | None = None
    last_login_date: datetime | None = None
    last_api_token_use_date: datetime | None = None
    last_name: str | None = None
    legal_remember: bool | None = None
    phone: StakeholderPhone | None = None
    registration_date: datetime | None = None
    role: str | None = None
    session_key: str | None = None
    session_token: StakeholderSessionToken | None = None
    tours: StakeholderTours | None = None
