from .types import (
    Company,
    Trial,
)
from dynamodb.types import (
    Item,
)


def format_trial(item: Item) -> Trial:
    return Trial(
        completed=item["completed"],
        extension_date=item["extension_date"],
        extension_days=item["extension_days"],
        start_date=item["start_date"],
    )


def format_company(item: Item) -> Company:
    return Company(
        domain=item["pk"].split("#")[1],
        trial=format_trial(item["trial"]),
    )
