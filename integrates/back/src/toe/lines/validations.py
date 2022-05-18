from custom_exceptions import (
    InvalidModifiedDate,
)
from datetime import (
    datetime,
)
from newutils import (
    datetime as datetime_utils,
)


def validate_modified_date(modified_date: datetime) -> None:
    if modified_date > datetime_utils.get_now():
        raise InvalidModifiedDate()
