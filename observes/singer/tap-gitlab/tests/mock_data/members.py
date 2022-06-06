from datetime import (
    datetime,
)
from tap_gitlab.api2.members import (
    Member,
    User,
    UserId,
)

mock_user = (
    UserId(5234),
    User(
        "avatar",
        "aang@airbender.com",
        "Aang",
        "active",
        datetime(1700, 1, 1),
        True,
    ),
)
mock_member = Member(mock_user, "active")
