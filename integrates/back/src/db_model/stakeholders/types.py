from typing import (
    NamedTuple,
    Optional,
)


class NotificationsPreferences(NamedTuple):
    email: list[str] = []


class StakeholderAccessToken(NamedTuple):
    iat: int
    jti: str
    salt: str


class StakeholderPhone(NamedTuple):
    country_code: str
    calling_country_code: str
    national_number: str


class StakeholderTours(NamedTuple):
    new_group: bool = False
    new_root: bool = False


class Stakeholder(NamedTuple):
    email: str
    first_name: str
    last_name: str
    access_token: Optional[StakeholderAccessToken] = None
    is_concurrent_session: bool = False
    last_login_date: Optional[str] = None
    legal_remember: bool = False
    notifications_preferences: NotificationsPreferences = (
        NotificationsPreferences()
    )
    phone: Optional[StakeholderPhone] = None
    push_tokens: Optional[list[str]] = None
    registration_date: Optional[str] = None
    tours: StakeholderTours = StakeholderTours()
