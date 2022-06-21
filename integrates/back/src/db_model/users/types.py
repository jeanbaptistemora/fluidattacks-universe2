from typing import (
    NamedTuple,
)


class NotificationsPreferences(NamedTuple):
    email: list[str]


class Stakeholder(NamedTuple):
    email: str
    notifications_preferences: NotificationsPreferences
