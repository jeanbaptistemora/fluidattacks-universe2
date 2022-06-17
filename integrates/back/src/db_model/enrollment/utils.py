from .types import (
    Enrollment,
    Trial,
)
from dynamodb.types import (
    Item,
)


def format_enrollment(item: Item) -> Enrollment:
    return Enrollment(
        email=item["email"],
        enrolled=item["enrolled"],
        trial=format_trial(item["trial"]),
    )


def format_trial(item: Item) -> Trial:
    return Trial(
        completed=item["completed"],
        extension_date=item["extension_date"],
        extension_days=item["extension_days"],
        start_date=item["start_date"],
    )
