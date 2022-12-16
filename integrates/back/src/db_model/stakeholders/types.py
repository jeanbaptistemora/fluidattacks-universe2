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
    Optional,
)


class NotificationsParameters(NamedTuple):
    min_severity: Decimal = Decimal("7.0")


class NotificationsPreferences(NamedTuple):
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


class StakeholderState(NamedTuple):
    modified_by: Optional[str]
    modified_date: Optional[datetime]
    notifications_preferences: NotificationsPreferences = (
        NotificationsPreferences()
    )


class Stakeholder(NamedTuple):
    email: str
    access_token: Optional[StakeholderAccessToken] = None
    first_name: Optional[str] = None
    is_concurrent_session: bool = False
    is_registered: bool = False
    last_login_date: Optional[datetime] = None
    last_name: Optional[str] = None
    legal_remember: bool = False
    phone: Optional[StakeholderPhone] = None
    registration_date: Optional[str] = None
    role: Optional[str] = None
    session_key: Optional[str] = None
    session_token: Optional[StakeholderSessionToken] = None
    state: StakeholderState = StakeholderState(
        notifications_preferences=NotificationsPreferences(),
        modified_by=None,
        modified_date=None,
    )
    tours: StakeholderTours = StakeholderTours()


class StakeholderMetadataToUpdate(NamedTuple):
    access_token: Optional[StakeholderAccessToken] = None
    first_name: Optional[str] = None
    is_concurrent_session: Optional[bool] = None
    is_registered: Optional[bool] = None
    last_login_date: Optional[datetime] = None
    last_name: Optional[str] = None
    legal_remember: Optional[bool] = None
    phone: Optional[StakeholderPhone] = None
    registration_date: Optional[str] = None
    role: Optional[str] = None
    session_key: Optional[str] = None
    session_token: Optional[StakeholderSessionToken] = None
    tours: Optional[StakeholderTours] = None
