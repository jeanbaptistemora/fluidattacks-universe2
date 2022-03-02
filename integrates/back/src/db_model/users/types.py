from typing import (
    List,
    NamedTuple,
)


class NotificationsPreferences(NamedTuple):
    email: List[str]


class User(NamedTuple):
    email: str
    notifications_preferences: NotificationsPreferences
