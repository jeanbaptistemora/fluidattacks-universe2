from custom_exceptions import (
    InvalidModifiedDate,
    InvalidSortsRiskLevel,
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


def validate_sort_risk_level(value: int) -> None:
    if not 0 <= value <= 100:
        raise InvalidSortsRiskLevel.new()
