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
    invitation_state: Optional[str] = None
    is_concurrent_session: bool = False
    is_registered: bool = False
    last_login_date: Optional[str] = None
    legal_remember: bool = False
    notifications_preferences: NotificationsPreferences = (
        NotificationsPreferences()
    )
    phone: Optional[StakeholderPhone] = None
    push_tokens: Optional[list[str]] = None
    registration_date: Optional[str] = None
    responsibility: Optional[str] = None
    role: Optional[str] = None
    tours: StakeholderTours = StakeholderTours()


class StakeholderMetadataToUpdate(NamedTuple):
    tours: Optional[StakeholderTours] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[StakeholderPhone] = None
    registration_date: Optional[str] = None
    last_login_date: Optional[str] = None
    legal_remember: Optional[bool] = None
    is_concurrent_session: Optional[bool] = None
    is_registered: Optional[bool] = None
    notifications_preferences: Optional[NotificationsPreferences] = None
    push_tokens: Optional[list[str]] = None
    access_token: Optional[StakeholderAccessToken] = None
