from typing import (
    Any,
    Dict,
    NamedTuple,
)


class User(NamedTuple):
    notifications_preferences: Dict[str, Any]
